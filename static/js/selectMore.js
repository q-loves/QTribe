layui.use(['form', 'element'], function() {
	var form = layui.form,
		element = layui.element;

	var province = $(".province");

	//初始将省份数据赋予
	for (var i = 0; i < provinceList.length; i++) {
		addEle(province, provinceList[i].name);
	}

	//向select中 追加内容
	function addEle(ele, value) {
		var optionStr = "";
		optionStr = "<option value=" + value + " >" + value + "</option>";
		ele.append(optionStr);
	}

	//重新渲染select
	form.render('select');

	//移除select中所有项
	function removeEle(ele) {
		ele.find("option").remove();
		var optionStar = "<option value=''>" + "请选择" + "</option>";
		ele.append(optionStar);
	}

	var provinceText,
		cityText,
		cityItem;
	//选定省份后 将该省份的数据读取追加上	
	form.on('select(province)', function(data) {
		var city = $(data.elem).parents(".layui-form-item").find(".city"),
			district = $(data.elem).parents(".layui-form-item").find(".district");
		provinceText = data.value;
		$.each(provinceList, function(i, item) {
			if (provinceText == item.name) {
				cityItem = i;
				return cityItem;
			}
		});
		removeEle(city);
		removeEle(district);
		$.each(provinceList[cityItem].cityList, function(i, item) {
			addEle(city, item.name);
		})
		form.render('select');
	})

	//选定后 将对应的数据读取追加上
	form.on('select(city)', function(data) {
		var district = $(data.elem).parents(".layui-form-item").find(".district");
		cityText = data.value;
		removeEle(district);
		$.each(provinceList, function(i, item) {
			if (provinceText == item.name) {
				cityItem = i;
				return cityItem;
			}
		});
		$.each(provinceList[cityItem].cityList, function(i, item) {
			if (cityText == item.name) {
				for (var n = 0; n < item.areaList.length; n++) {
					addEle(district, item.areaList[n]);
				}
			}
		})
		form.render('select');
	})



})
