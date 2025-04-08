// 获取用户当前地理位置并查询天气

// function getLocation() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition((position) => {
//             const lat = position.coords.latitude;
//             const lon = position.coords.longitude;
//
//             // AJAX 异步请求 GPS 接口
//             fetch(`/gps?lat=${lat}&lon=${lon}`)
//                 .then(response => {
//                     if (response.ok) {
//                         // 请求成功后刷新首页，重新获取天气数据
//                         window.location.href = "/";
//                     } else {
//                         alert("获取本地天气失败");
//                     }
//                 })
//                 .catch(() => {
//                     alert("请求错误，请稍后再试");
//                 });
//
//         }, () => {
//             alert("无法获取位置信息");
//         });
//     } else {
//         alert("你的浏览器不支持地理位置获取");
//     }
// }

/*
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            // 用 fetch 请求本地天气数据，不跳转页面
            fetch(`/gps?lat=${lat}&lon=${lon}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('网络请求失败');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        alert(`错误：${data.error}`);
                    } else {
                        updateWeatherDisplay(data);
                    }
                })
                .catch(error => {
                    alert("获取本地天气失败，请稍后再试！");
                    console.error(error);
                });

        }, () => {
            alert("无法获取位置信息");
        });
    } else {
        alert("你的浏览器不支持地理位置获取");
    }
}
 */

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            // 不再用 fetch，而是跳转（因为后端已改为返回完整页面）
            window.location.href = `/gps?lat=${lat}&lon=${lon}`;
        }, () => {
            alert("Unable to get location information");
        });
    } else {
        alert("Your browser doesn't support geolocation fetching");
    }
}


// 提交查询表单
function submitForm(event) {
    event.preventDefault(); // 阻止表单默认提交行为

    const location = document.querySelector("input[name='location']").value;
    if (location.trim() === "") {
        alert("Please enter a valid location!");
        return;
    }

    // 使用AJAX向后端请求天气数据
    fetch(`/weather?location=${encodeURIComponent(location)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Wrong：${data.error}`);
            } else {
                updateWeatherDisplay(data);
            }
        })
        .catch(error => {
            alert("The request failed, please try again later!");
            console.error("City weather fetch failed", error);
        });
}

// 更新页面上的天气显示
function updateWeatherDisplay(data) {
    const weatherContainer = document.getElementById('weather-info');
    const forecastContainer = document.getElementById('forecast-info');

    // 显示当前天气
    weatherContainer.innerHTML = `
        <h3>${data.location}</h3>
        <p>
            <img class="weather-icon" src="${data.icon}" alt="天气图标">
            ${data.description}，${data.temperature}°C
        </p>
    `;

    // 清空并展示五日预报
    forecastContainer.innerHTML = '';
    if (data.forecast && data.forecast.length > 0) {
        data.forecast.forEach(day => {
            const forecastElement = document.createElement('div');
            forecastElement.classList.add('forecast-item');
            forecastElement.innerHTML = `
                <strong>${day.date}</strong>
                <img class="weather-icon" src="${day.icon}" alt="icon">
                <p>${day.description}</p>
                <p>${day.temp}°C</p>
            `;
            forecastContainer.appendChild(forecastElement);
        });
    }
}




// 页面加载后绑定事件
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', submitForm);
    }
     // 获取按钮并添加点击事件监听器
    document.getElementById('getWeatherButton').addEventListener('click', (event) => {
        event.preventDefault(); // 阻止按钮的默认行为
        getLocation(); // 调用获取位置和天气的函数
    });
});


