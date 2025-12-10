// API 基礎 URL
const API_BASE = '/api';

// 使用者 ID（實際應用中應該從 session 或登入狀態取得）
const USER_ID = 1;

// 店家資料（從 API 載入）
let storeData = [];

// --- 修正：初始化為空陣列 ---
let dailyDietData = [];

// 收藏狀態變數 (儲存 restaurant_id)
let favorites = [];
let currentStoreId = null;
let currentRestaurantId = null;

// 月曆狀態
let currentMonth = new Date();
let selectedDate = currentMonth.getDate();


// 頁面切換邏輯
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-item');
    const pageSections = document.querySelectorAll('.page-section');
    const followIcon = document.getElementById('follow-icon');
    const categoryButtons = document.querySelectorAll('.category-filters .filter-btn');
    const priceButtons = document.querySelectorAll('.price-filters .filter-btn');
    const vegetarianToggle = document.getElementById('vegetarian-toggle');
    const resetFiltersButton = document.getElementById('reset-filters');
    const storeListContainer = document.getElementById('store-list-container');

    // 我的飲食頁面元素
    const monthYearDisplay = document.getElementById('current-month-year');
    const calendarGrid = document.getElementById('calendar-grid');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const mealButtons = document.querySelectorAll('.meal-card-btn');
    const mealDetailContainer = document.getElementById('meal-detail-container');
    const totalSummaryContainer = document.getElementById('total-summary');
    const mealSummaryTitle = document.getElementById('meal-summary-title');
    const mealSummaryValues = document.getElementById('meal-summary-values');
    const mealFoodList = document.getElementById('meal-food-list');
    const totalSummaryValues = document.getElementById('total-summary-values');
    const totalFoodList = document.getElementById('total-food-list');
    const saveDietBtn = document.getElementById('save-diet-btn');
    const deleteDietBtn = document.getElementById('delete-diet-btn');

    // 輸入框元素
    const foodNameInput = document.getElementById('food-name');
    const foodImageInput = document.getElementById('food-image-input');
    const uploadImageBtn = document.getElementById('upload-image-btn');
    const uploadBtnText = document.getElementById('upload-btn-text');
    // const portionSizeInput = document.getElementById('portion-size'); // Removed
    const inputCals = document.getElementById('food-cals');
    const inputCarbs = document.getElementById('food-carbs');
    const inputProtein = document.getElementById('food-protein');
    const inputFat = document.getElementById('food-fat');
    const inputSugar = document.getElementById('food-sugar');
    const inputSodium = document.getElementById('food-sodium');

    // 上傳圖片按鈕邏輯
    if (uploadImageBtn) {
        uploadImageBtn.addEventListener('click', () => {
            foodImageInput.click();
        });
    }

    if (foodImageInput) {
        foodImageInput.addEventListener('change', () => {
            if (foodImageInput.files && foodImageInput.files[0]) {
                uploadBtnText.textContent = foodImageInput.files[0].name;
            } else {
                uploadBtnText.textContent = '上傳圖片';
            }
        });
    }


    // --- 輔助函式定義 ---

    function setActivePage(targetId, navId, storeId = null) {
        pageSections.forEach(section => section.classList.remove('active'));
        const targetSection = document.getElementById(targetId);
        if (targetSection) targetSection.classList.add('active');

        navLinks.forEach(link => link.classList.remove('selected'));
        const navElement = document.getElementById(navId);
        if (navElement) navElement.classList.add('selected');

        if (targetId === 'store-detail-page' && storeId !== null) {
            loadStoreDetail(storeId);
        } else if (targetId === 'diet-page') {
            renderCalendar(currentMonth);
            resetMealView();
            loadDietData();
        } else if (targetId === 'favorite-page') {
            loadFavorites();
        }
    }

    // API 呼叫函式
    async function fetchStores(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.keyword) params.append('keyword', filters.keyword);
            if (filters.categories && filters.categories.length > 0) {
                params.append('categories', filters.categories.join(','));
            }
            if (filters.price) params.append('price', filters.price);
            if (filters.vegetarian) params.append('vegetarian', 'true');
            params.append('user_id', USER_ID);

            const response = await fetch(`${API_BASE}/stores?${params.toString()}`);
            const result = await response.json();

            if (result.success) {
                return result.data;
            } else {
                console.error('取得餐廳列表失敗:', result.error);
                return [];
            }
        } catch (error) {
            console.error('API 錯誤:', error);
            return [];
        }
    }

    async function fetchStoreDetail(storeId) {
        try {
            const response = await fetch(`${API_BASE}/stores/${storeId}?user_id=${USER_ID}`);
            const result = await response.json();

            if (result.success) {
                return result.data;
            } else {
                console.error('取得餐廳詳情失敗:', result.error);
                return null;
            }
        } catch (error) {
            console.error('API 錯誤:', error);
            return null;
        }
    }

    async function fetchFavorites() {
        try {
            const response = await fetch(`${API_BASE}/favorites?user_id=${USER_ID}`);
            const result = await response.json();

            if (result.success) {
                return result.data;
            } else {
                console.error('取得收藏列表失敗:', result.error);
                return [];
            }
        } catch (error) {
            console.error('API 錯誤:', error);
            return [];
        }
    }

    async function addFavorite(restaurantId) {
        try {
            const response = await fetch(`${API_BASE}/favorites`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: USER_ID,
                    restaurant_id: restaurantId
                })
            });
            const result = await response.json();
            return result.success;
        } catch (error) {
            console.error('API 錯誤:', error);
            return false;
        }
    }

    async function removeFavorite(restaurantId) {
        try {
            const response = await fetch(`${API_BASE}/favorites`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: USER_ID,
                    restaurant_id: restaurantId
                })
            });
            const result = await response.json();
            return result.success;
        } catch (error) {
            console.error('API 錯誤:', error);
            return false;
        }
    }

    // --- LocalStorage 存取函式 ---

    function getLocalDietLogs() {
        const logs = localStorage.getItem('diet_logs');
        return logs ? JSON.parse(logs) : [];
    }

    function saveLocalDietLogs(logs) {
        localStorage.setItem('diet_logs', JSON.stringify(logs));
    }

    // 暴露給全域使用，以便 onclick 可以呼叫
    window.deleteLocalDietLog = function(id) {
        if (!confirm('確定要刪除這筆紀錄嗎？')) return;
        
        let logs = getLocalDietLogs();
        logs = logs.filter(log => log.id !== id);
        saveLocalDietLogs(logs);
        
        // 重新載入
        loadDietData();
    }

    // 將圖片轉為 Base64
    function convertImageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }

    async function loadDietData() {
        const selectedDateElement = document.querySelector('.cal-day.selected');
        let date = null;
        if (selectedDateElement) {
            const dateStr = selectedDateElement.getAttribute('data-date');
            if (dateStr) {
                const dateObj = new Date(dateStr);
                date = dateObj.toISOString().split('T')[0];
            }
        }
        if (!date) {
            date = new Date().toISOString().split('T')[0];
        }

        // 從 LocalStorage 讀取並篩選日期
        const allLogs = getLocalDietLogs();
        dailyDietData = allLogs.filter(log => log.date === date);
        
        renderTotalSummary(dailyDietData);
        
        // 如果正在查看特定餐次，也要更新該餐次的顯示
        const selectedBtn = document.querySelector('.meal-card-btn.selected');
        if (selectedBtn) {
            const mealType = selectedBtn.getAttribute('data-meal');
            renderMealDetails(mealType, dailyDietData);
        }
    }

    // 移除舊的 fetchDietLogs 和 saveDietLog API 呼叫
    // async function fetchDietLogs... (已移除)
    // async function saveDietLog... (已移除)

    function resetAllFilters() {
        categoryButtons.forEach(button => {
            button.classList.remove('selected');
        });
        priceButtons.forEach(button => {
            button.classList.remove('selected');
        });
        if (vegetarianToggle) {
            vegetarianToggle.checked = false;
        }
        console.log("分類及價格篩選條件已重置。");
        loadStores();
    }

    async function loadStores() {
        const selectedCategories = Array.from(categoryButtons)
            .filter(btn => btn.classList.contains('selected'))
            .map(btn => btn.textContent);
        const selectedPrice = Array.from(priceButtons)
            .find(btn => btn.classList.contains('selected'))?.textContent || '';
        const isVegetarian = vegetarianToggle?.checked || false;
        const keyword = document.querySelector('.search-input-group input')?.value || '';

        storeData = await fetchStores({
            keyword: keyword,
            categories: selectedCategories,
            price: selectedPrice,
            vegetarian: isVegetarian
        });

        renderStoreList(storeData);
    }

    function renderTotalSummary(data) {
        const total = data.reduce((acc, item) => {
            acc.cals += item.cals || 0;
            acc.carbs += item.carbs || 0;
            acc.protein += item.protein || 0;
            acc.fat += item.fat || 0;
            acc.sugar += item.sugar || 0;
            acc.sodium += item.sodium || 0;
            return acc;
        }, { cals: 0, carbs: 0, protein: 0, fat: 0, sugar: 0, sodium: 0 });

        totalSummaryValues.innerHTML = `
            <div class="summary-value"><p>${total.cals}</p><p>大卡</p></div>
            <div class="summary-value"><p>${total.carbs}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.protein}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.fat}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.sugar}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.sodium}</p><p>毫克</p></div>
        `;

        if (totalFoodList) {
            if (data.length === 0) {
                totalFoodList.innerHTML = '<p style="text-align: center; color: #999;">今日尚未新增資料</p>';
            } else {
                totalFoodList.innerHTML = data.map(item => `
                    <div class="food-entry">
                        <div class="entry-title">
                            ${item.name} 
                            <span style="font-size: 0.8em; color: #666; margin-left: 10px;">
                                (${getMealName(item.meal)})
                            </span>
                            <button onclick="deleteLocalDietLog(${item.id})" style="float: right; background: none; border: none; color: #ff4d4f; cursor: pointer;">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </div>
                        ${item.image ? `<img src="${item.image}" style="max-width: 100px; max-height: 100px; margin: 5px 0; border-radius: 5px;">` : ''}
                        <div class="entry-nutrients">
                            <div class="entry-nutrient"><p>${item.cals}</p><p>大卡</p></div>
                            <div class="entry-nutrient"><p>${item.carbs}</p><p>公克</p></div>
                            <div class="entry-nutrient"><p>${item.protein}</p><p>公克</p></div>
                            <div class="entry-nutrient"><p>${item.fat}</p><p>公克</p></div>
                            <div class="entry-nutrient"><p>${item.sugar}</p><p>公克</p></div>
                            <div class="entry-nutrient"><p>${item.sodium}</p><p>毫克</p></div>
                        </div>
                    </div>
                `).join('');
            }
        }

        mealButtons.forEach(btn => {
            const mealType = btn.getAttribute('data-meal');
            const mealCals = data
                .filter(item => item.meal === mealType)
                .reduce((sum, item) => sum + (item.cals || 0), 0);
            btn.querySelector('.meal-cal-summary').textContent = `已攝取：約 ${mealCals} 大卡`;
        });
    }

    function renderMealDetails(mealType, data) {
        const mealItems = data.filter(item => item.meal === mealType);

        const total = mealItems.reduce((acc, item) => {
            acc.cals += item.cals || 0;
            acc.carbs += item.carbs || 0;
            acc.protein += item.protein || 0;
            acc.fat += item.fat || 0;
            acc.sugar += item.sugar || 0;
            acc.sodium += item.sodium || 0;
            return acc;
        }, { cals: 0, carbs: 0, protein: 0, fat: 0, sugar: 0, sodium: 0 });

        mealSummaryTitle.textContent = getMealName(mealType) + ' 攝取量'; // 顯示中文名稱
        mealSummaryValues.innerHTML = `
            <div class="summary-value"><p>${total.cals}</p><p>大卡</p></div>
            <div class="summary-value"><p>${total.carbs}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.protein}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.fat}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.sugar}</p><p>公克</p></div>
            <div class="summary-value"><p>${total.sodium}</p><p>毫克</p></div>
        `;

        if (mealItems.length === 0) {
            mealFoodList.innerHTML = '<p style="text-align: center; color: #999;">尚未新增資料</p>';
        } else {
            mealFoodList.innerHTML = mealItems.map(item => `
                <div class="food-entry">
                    <div class="entry-title">
                        ${item.name}
                        <button onclick="deleteLocalDietLog(${item.id})" style="float: right; background: none; border: none; color: #ff4d4f; cursor: pointer;">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                    ${item.image ? `<img src="${item.image}" style="max-width: 100px; max-height: 100px; margin: 5px 0; border-radius: 5px;">` : ''}
                    <div class="entry-nutrients">
                        <div class="entry-nutrient"><p>${item.cals}</p><p>大卡</p></div>
                        <div class="entry-nutrient"><p>${item.carbs}</p><p>公克</p></div>
                        <div class="entry-nutrient"><p>${item.protein}</p><p>公克</p></div>
                        <div class="entry-nutrient"><p>${item.fat}</p><p>公克</p></div>
                        <div class="entry-nutrient"><p>${item.sugar}</p><p>公克</p></div>
                        <div class="entry-nutrient"><p>${item.sodium}</p><p>毫克</p></div>
                    </div>
                </div>
            `).join('');
        }
    }

    function getMealName(type) {
        switch (type) {
            case 'breakfast': return '早餐';
            case 'lunch': return '午餐';
            case 'dinner': return '晚餐';
            case 'other': return '其他';
            default: return type;
        }
    }

    function resetMealView() {
        totalSummaryContainer.style.display = 'block';
        mealDetailContainer.style.display = 'none';
        document.getElementById('diet-form').style.display = 'none'; // 隱藏輸入表單
        mealButtons.forEach(btn => btn.classList.remove('selected'));
        renderTotalSummary(dailyDietData); // 確保每次重置都更新總計
    }

    // --- 儲存功能 (LocalStorage) ---
    saveDietBtn.addEventListener('click', async () => {
        // 找出當前選中的餐次
        const selectedBtn = document.querySelector('.meal-card-btn.selected');
        if (!selectedBtn) {
            alert('請先選擇一個餐次！');
            return;
        }
        const mealType = selectedBtn.getAttribute('data-meal');

        // 獲取輸入值
        const foodName = foodNameInput.value.trim();
        const portionSize = 1.0; // Default to 1.0 as input is removed
        
        if (!foodName) {
            alert('請輸入餐點名稱！');
            return;
        }

        // 處理圖片
        let imageBase64 = null;
        if (foodImageInput.files && foodImageInput.files[0]) {
            try {
                imageBase64 = await convertImageToBase64(foodImageInput.files[0]);
            } catch (e) {
                console.error("圖片轉換失敗", e);
                alert("圖片上傳失敗");
                return;
            }
        }

        // 取得選中的日期
        const selectedDateElement = document.querySelector('.cal-day.selected');
        let date = null;
        if (selectedDateElement) {
            const dateStr = selectedDateElement.getAttribute('data-date');
            if (dateStr) {
                const dateObj = new Date(dateStr);
                date = dateObj.toISOString().split('T')[0];
            }
        }
        if (!date) {
            date = new Date().toISOString().split('T')[0];
        }

        // 建構新紀錄物件
        const newLog = {
            id: Date.now(), // 使用 timestamp 當作 ID
            date: date,
            meal: mealType,
            name: foodName,
            portion_size: portionSize,
            cals: parseFloat(inputCals.value) || 0,
            carbs: parseFloat(inputCarbs.value) || 0,
            protein: parseFloat(inputProtein.value) || 0,
            fat: parseFloat(inputFat.value) || 0,
            sugar: parseFloat(inputSugar.value) || 0,
            sodium: parseFloat(inputSodium.value) || 0,
            image: imageBase64
        };

        // 儲存到 LocalStorage
        const logs = getLocalDietLogs();
        logs.push(newLog);
        saveLocalDietLogs(logs);

        // 重新載入飲食數據
        await loadDietData();

        // 重置輸入框
        foodNameInput.value = '';
        foodImageInput.value = ''; // 清除檔案選擇
        if (uploadBtnText) uploadBtnText.textContent = '上傳圖片';
        // portionSizeInput.value = '1.0';
        inputCals.value = '';
        inputCarbs.value = '';
        inputProtein.value = '';
        inputFat.value = '';
        inputSugar.value = '';
        inputSodium.value = '';

        console.log('已儲存至 LocalStorage:', newLog);
    });

    // --- 重置/刪除功能 ---
    if (deleteDietBtn) {
        deleteDietBtn.addEventListener('click', () => {
            foodNameInput.value = '';
            foodImageInput.value = '';
            if (uploadBtnText) uploadBtnText.textContent = '上傳圖片';
            // portionSizeInput.value = '1.0';
            inputCals.value = '';
            inputCarbs.value = '';
            inputProtein.value = '';
            inputFat.value = '';
            inputSugar.value = '';
            inputSodium.value = '';
        });
    }

    async function loadStoreDetail(storeId) {
        const store = await fetchStoreDetail(storeId);
        if (store) {
            currentStoreId = store.id;
            currentRestaurantId = store.restaurant_id;
            renderStoreDetail(store);
        }
    }

    async function loadFavorites() {
        const favoriteStores = await fetchFavorites();
        favorites = favoriteStores.map(s => s.restaurant_id);
        renderFavorites(favoriteStores);
    }




    async function handleDayClick() {
        document.querySelectorAll('#calendar-grid .cal-day').forEach(day => day.classList.remove('selected'));
        this.classList.add('selected');

        const selectedDateStr = this.getAttribute('data-date');
        selectedDate = parseInt(this.textContent);
        console.log(`日期 ${selectedDateStr} 被選中。`);

        // 載入該日期的飲食數據
        await loadDietData();
        resetMealView();
    }

    async function handleMealClick() {
        const mealType = this.getAttribute('data-meal');
        const isSelected = this.classList.contains('selected');

        mealButtons.forEach(btn => btn.classList.remove('selected'));

        if (!isSelected) {
            this.classList.add('selected');
            totalSummaryContainer.style.display = 'none';
            mealDetailContainer.style.display = 'block';
            document.getElementById('diet-form').style.display = 'block';

            // 載入該餐次的數據
            const selectedDateElement = document.querySelector('.cal-day.selected');
            let date = null;
            if (selectedDateElement) {
                const dateStr = selectedDateElement.getAttribute('data-date');
                if (dateStr) {
                    const dateObj = new Date(dateStr);
                    date = dateObj.toISOString().split('T')[0];
                }
            }
            if (!date) {
                date = new Date().toISOString().split('T')[0];
            }

            const allLogs = getLocalDietLogs();
            const mealData = allLogs.filter(log => log.date === date && log.meal === mealType);
            renderMealDetails(mealType, mealData);
            console.log(`正在查看 ${mealType} 詳情。`);
        } else {
            resetMealView();
            console.log(`返回總累積攝取視圖。`);
        }
    }


    function renderCalendar(date) {
        const now = new Date();
        const currentYear = now.getFullYear();
        const currentMonthIndex = now.getMonth();
        const todayDate = now.getDate();

        const year = date.getFullYear();
        const month = date.getMonth();

        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        monthYearDisplay.textContent = `${monthNames[month]} ${year}`;

        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const daysInPrevMonth = new Date(year, month, 0).getDate();

        calendarGrid.innerHTML = `
            <span class="cal-weekday">Su</span>
            <span class="cal-weekday">Mo</span>
            <span class="cal-weekday">Tu</span>
            <span class="cal-weekday">We</span>
            <span class="cal-weekday">Th</span>
            <span class="cal-weekday">Fr</span>
            <span class="cal-weekday">Sa</span>
        `;

        for (let i = firstDayOfMonth; i > 0; i--) {
            const day = daysInPrevMonth - i + 1;
            const dayElement = document.createElement('span');
            dayElement.classList.add('cal-day', 'not-in-month');
            dayElement.textContent = day;
            calendarGrid.appendChild(dayElement);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dateString = `${monthNames[month]} ${day}, ${year}`;
            const dayElement = document.createElement('span');
            dayElement.classList.add('cal-day', 'in-month');
            dayElement.textContent = day;
            dayElement.setAttribute('data-date', dateString);

            const isToday = year === currentYear && month === currentMonthIndex && day === todayDate;

            if (isToday) {
                dayElement.classList.add('selected');
            } else if (day === selectedDate && year === currentMonth.getFullYear() && month === currentMonth.getMonth()) {
                dayElement.classList.add('selected');
            }

            dayElement.addEventListener('click', handleDayClick);
            calendarGrid.appendChild(dayElement);
        }

        const totalCells = firstDayOfMonth + daysInMonth;
        const cellsNeeded = 42;
        let nextDay = 1;

        for (let i = totalCells; i < cellsNeeded; i++) {
            const dayElement = document.createElement('span');
            dayElement.classList.add('cal-day', 'not-in-month');
            dayElement.textContent = nextDay++;
            calendarGrid.appendChild(dayElement);
        }
    }

    function changeMonth(delta) {
        currentMonth.setDate(1);
        currentMonth.setMonth(currentMonth.getMonth() + delta);
        currentMonth.setDate(Math.min(selectedDate, new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate()));
        renderCalendar(currentMonth);
    }

    function renderStoreList(stores) {
        // Ensure storeListContainer exists before trying to access innerHTML
        const container = document.getElementById('store-list-container') || storeListContainer;
        if (!container) {
            console.error("Store list container not found!");
            return;
        }

        container.innerHTML = '';

        if (!stores || stores.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666; padding: 40px 0;">沒有找到符合條件的餐廳。</p>';
            return;
        }

        stores.forEach(store => {
            const card = document.createElement('a');
            card.href = '#';
            card.classList.add('store-card', 'store-link');
            card.setAttribute('data-store-id', store.id || store.restaurant_id);

            card.innerHTML = `
                <img src="${store.heroImg || 'placeholder-store-1.jpg'}" alt="${store.name}">
                <div class="store-info">
                    <p class="store-name">${store.name}</p>
                    <span class="distance">${store.distance || '0.8 km'}</span>
                </div>
                <div class="store-rating">
                    <span class="stars">${store.rating ? store.rating.split(' ')[0] : '★★★★☆'}</span>
                    <span class="price-range">${store.priceRange || '$ 1 ~ 200'}</span>
                </div>
            `;
            container.appendChild(card);
        });

        container.querySelectorAll('.store-link').forEach(link => {
            link.addEventListener('click', handleStoreLinkClick);
        });
    }

    function handleStoreLinkClick(e) {
        e.preventDefault();
        const storeId = this.getAttribute('data-store-id');
        setActivePage('store-detail-page', 'nav-search', storeId);
    }


    function renderStoreDetail(store) {
        document.getElementById('detail-hero-img').src = store.heroImg || 'placeholder-store-1.jpg';
        document.getElementById('detail-hero-img').alt = store.name;
        document.getElementById('detail-description').textContent = store.description || store.name;

        const starRating = store.rating ? store.rating.split(' ')[0] : '★★★★☆';
        const metaText = store.rating || '★★★★☆ 4.0';

        document.getElementById('detail-rating-stars').innerHTML = `<i class="fa-solid fa-star"></i> ${metaText}`;
        document.getElementById('detail-price-meta').textContent = store.priceMeta || '$';
        document.getElementById('detail-distance').textContent = store.distance || '0.8 km';
        document.getElementById('detail-address').textContent = store.address || '';

        const menuContainer = document.getElementById('detail-menu-cards');
        menuContainer.innerHTML = '';

        if (store.menu && store.menu.length > 0) {
            store.menu.forEach((item, index) => {
                // 使用本地圖片（循環使用 20 張）
                const imgIndex = (index % 20) + 1;
                const placeholderImg = `/static/images/dishes/dish_${imgIndex}.jpg`;
                const menuCard = document.createElement('div');
                menuCard.classList.add('menu-card');
                menuCard.innerHTML = `
                    <img src="${placeholderImg}" alt="${item.name}">
                    <p>${item.name}</p>
                    <span>${item.price}</span>
                `;
                menuContainer.appendChild(menuCard);
            });
        } else {
            menuContainer.innerHTML = '<p style="text-align: center; color: #999;">暫無菜單資訊</p>';
        }

        const isFavorited = store.is_favorited || favorites.includes(store.restaurant_id);
        if (followIcon) {
            if (isFavorited) {
                followIcon.classList.remove('fa-regular');
                followIcon.classList.add('fa-solid', 'followed');
            } else {
                followIcon.classList.remove('fa-solid', 'followed');
                followIcon.classList.add('fa-regular');
            }
        }
    }

    function renderFavorites(favoriteStores = null) {
        const container = document.getElementById('favorite-list-container');
        container.innerHTML = '';

        if (!favoriteStores) {
            favoriteStores = storeData.filter(store => favorites.includes(store.restaurant_id || store.id));
        }

        if (favoriteStores.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666; padding: 40px 0;">您的收藏列表是空的。</p>';
            return;
        }

        favoriteStores.forEach(store => {
            const card = document.createElement('a');
            card.href = '#';
            card.classList.add('store-card', 'store-link');
            card.setAttribute('data-store-id', store.id || store.restaurant_id);

            card.innerHTML = `
                <img src="${store.heroImg || 'placeholder-store-1.jpg'}" alt="${store.name}">
                <div class="store-info">
                    <p class="store-name">${store.name}</p>
                    <span class="distance">${store.distance || '0.8 km'}</span>
                </div>
                <div class="store-rating">
                    <span class="stars">${store.rating ? store.rating.split(' ')[0] : '★★★★☆'}</span>
                    <span class="price-range">${store.priceRange || '$ 1 ~ 200'}</span>
                </div>
            `;
            container.appendChild(card);
        });

        document.querySelectorAll('.store-link').forEach(link => {
            link.addEventListener('click', handleStoreLinkClick);
        });
    }


    // --- 執行初始化和事件綁定 ---

    // 初始載入和綁定
    prevMonthBtn.addEventListener('click', () => changeMonth(-1));
    nextMonthBtn.addEventListener('click', () => changeMonth(1));
    mealButtons.forEach(button => {
        button.addEventListener('click', handleMealClick);
    });
    resetFiltersButton.addEventListener('click', resetAllFilters);

    // 導覽列點擊事件
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetPage = link.getAttribute('data-page');
            setActivePage(targetPage, link.id);
        });
    });

    // 追蹤圖標點擊事件 (愛心切換 & 不跳轉)
    if (followIcon) {
        followIcon.addEventListener('click', async (e) => {
            e.preventDefault();

            if (!currentRestaurantId) return; // 確保有餐廳 ID

            const isFavorited = followIcon.classList.contains('fa-solid');

            if (!isFavorited) {
                // 加入收藏
                const success = await addFavorite(currentRestaurantId);
                if (success) {
                    favorites.push(currentRestaurantId);
                    followIcon.classList.remove('fa-regular');
                    followIcon.classList.add('fa-solid', 'followed');
                    console.log(`店家 ${currentRestaurantId} 已收藏。`);
                }
            } else {
                // 移除收藏
                const success = await removeFavorite(currentRestaurantId);
                if (success) {
                    favorites = favorites.filter(id => id !== currentRestaurantId);
                    followIcon.classList.remove('fa-solid', 'followed');
                    followIcon.classList.add('fa-regular');
                    console.log(`店家 ${currentRestaurantId} 已取消收藏。`);
                }
            }
        });
    }

    // 搜尋按鈕事件
    const searchButton = document.querySelector('.search-bar-section .btn-primary');
    if (searchButton) {
        searchButton.addEventListener('click', () => {
            loadStores();
        });
    }

    // 搜尋輸入框 Enter 鍵事件
    const searchInput = document.querySelector('.search-input-group input');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                loadStores();
            }
        });
    }

    // 類別和價格篩選變更時重新載入
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('selected');
            loadStores();
        });
    });

    priceButtons.forEach(button => {
        button.addEventListener('click', () => {
            const isSelected = button.classList.contains('selected');
            priceButtons.forEach(btn => btn.classList.remove('selected'));

            if (!isSelected) {
                button.classList.add('selected');
            }
            loadStores();
        });
    });

    // 素食開關變更時重新載入
    if (vegetarianToggle) {
        vegetarianToggle.addEventListener('change', () => {
            loadStores();
        });
    }

    // --- 啟動初始化 ---

    // 修正: 確保所有初始化相關函式在 DOMContentLoaded 綁定後被調用
    setActivePage('search-page', 'nav-search');
    loadStores(); // 載入餐廳列表
    renderTotalSummary(dailyDietData);
    mealDetailContainer.style.display = 'none';
});

// 飲食輸入表單切換邏輯 (Frame 3/5)
function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}