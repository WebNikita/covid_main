function creatmap(lat, lon, json_with_lat_lon) {
    var myMap = new ymaps.Map("map", {
            center: [lat, lon],
            zoom: 15
        }, {
            searchControlProvider: 'yandex#search',
            controls: ['routePanelControl']
        })
    var myCircle = new ymaps.Circle([
        // Координаты центра круга.
        [lat, lon],
        // Радиус круга в метрах.
        1000
    ], {
        // Описываем свойства круга.
        // Содержимое балуна.
        balloonContent: "Шаговая доступность 2км",
    }, {
        // Задаем опции круга.
        // Включаем возможность перетаскивания круга.
        draggable: false,
        // Цвет заливки.
        // Последний байт (77) определяет прозрачность.
        // Прозрачность заливки также можно задать используя опцию "fillOpacity".
        fillColor: "#DB709377",
        // Цвет обводки.
        strokeColor: "#990066",
        // Прозрачность обводки.
        strokeOpacity: 0.8,
        // Ширина обводки в пикселях.
        strokeWidth: 4
    });
    // for(var i = 0; i < json_with_lat_lon.length; i++) {
    //     myMap.geoObjects.add(new ymaps.Placemark([json_with_lat_lon[0][1],json_with_lat_lon[0][0]]))
    // }
    console.log(json_with_lat_lon[0])
    myMap.geoObjects
        .add(myCircle)
        for(var i = 0; i < json_with_lat_lon.length; i++) {
            myMap.geoObjects
                        .add(new ymaps.Placemark([json_with_lat_lon[i][1],json_with_lat_lon[i][0]]))
        }      
}
function creatroute(lat, lon) {
    var myMap = new ymaps.Map("map_route", {
            center: [lat, lon],
            zoom: 15
        }, {
            searchControlProvider: 'yandex#search',
            controls: ['routePanelControl']
        })
    var multiRoute = new ymaps.multiRouter.MultiRoute({   
    // Точки маршрута. Точки могут быть заданы как координатами, так и адресом. 
    referencePoints: [
        [lat, lon],
        [56.008571, 37.199809],
    ]
    }, {
      // Автоматически устанавливать границы карты так,
      // чтобы маршрут был виден целиком.
        boundsAutoApply: true
    });

    // Добавление маршрута на карту.
    myMap.geoObjects.add(multiRoute);
    
}
