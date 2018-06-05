/**
 * 网络请求
 * @type {{}}
 */
var http = {};

/**Ajax*/
http.ajax = {};
http.ajax.CONTENT_TYPE_1 = 'application/x-www-form-urlencoded;charset=utf-8';
http.ajax.CONTENT_TYPE_2 = 'application/json;charset=utf-8';

/**GET请求*/
http.ajax.get = function (async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: 'GET',
        url: url,
        data: data,
        contentType: contentType,
        dataType: 'json',
        beforeSend: function () {
            layer.load(2, {offset: ['55%', '50%']});
        },
        complete: function (response) {
            if (response.status == 400) {
                layer.msg('请检查您输入的的数据');
                layer.closeAll('loading');
                return false;
            }
            if (response.status == 500) {
                layer.msg('服务器内部错误！');
                layer.closeAll('loading');
                return false;
            }else {
                layer.closeAll('loading')
            }

        },
        success: function (result) {
            if (typeof callback == 'function') {
                callback(result);
            }
        }
    });

};

http.ajax.get_no_loading = function (async, cache, url, data, contentType, callback, returnStatus) {
    $.ajax({
        async: async,
        cache: cache,
        type: 'GET',
        url: url,
        data: data,
        contentType: contentType,
        dataType: 'json',
        success: function (result) {
            if (typeof callback == 'function') {
                callback(result);
                return;
            }

        }
    });

};

/**POST请求*/
http.ajax.post = function (async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: 'POST',
        url: url,
        data: data,
        contentType: contentType,
        dataType: 'json',
        beforeSend: function () {
            layer.load(2, {offset: ['55%', '50%']});
        },
        complete: function (response) {
            if (response.status == 400) {
                layer.msg('请检查账号密码！');
                layer.closeAll('loading')
                return false;
            }
            if (response.status == 500) {
                layer.msg('服务器内部错误！');
                layer.closeAll('loading')
                return false;
            }else {
                layer.closeAll('loading')
            }
        },
        success: function (result) {
            if (typeof callback == 'function') {
                callback(result);
                return false;
            } else if (result.msg != null && result != '') {
                layer.msg('服务器异常' + result.msg);
            }
        }

    });

}
/**POST请求2*/
http.ajax.post_no_loading = function (async, cache, url, data, contentType, callback) {

    $.ajax({
        async: async,
        cache: cache,
        type: 'POST',
        url: url,
        data: data,
        contentType: contentType,
        dataType: 'json',
        success: function (result) {
            if (typeof callback == 'function') {
                if (result.success) {
                    callback(result);
                    return;
                }
            }
        }
    });

};

/**PATCH请求*/
http.ajax.patch = function (async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: 'PATCH',
        url: url,
        data: data,
        contentType: contentType,
        dataType: 'json',
        beforeSend: function () {
            layer.load(2, {offset: ['55%', '50%']});
        },
        complete: function () {
            layer.closeAll('loading');
        },
        success: function (result) {
            if (typeof callback == 'function') {
                if (result.success) {
                    callback(result);
                    return;
                }
                if (result.msg != null && result != '') {
                    layer.msg(result.msg);
                    return;
                }
                layer.msg('服务器异常');
            }
        }
    });

}