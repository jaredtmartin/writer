(function( $ ) {

var _parseNodes = function(map) {
    var nodes = {};
    $.each(map, function(key, selector){
        nodes[key] = $(selector);
    });
    return nodes;
}
var Highlighting =(function() {
    var TPL_MARKER = '<div class="srt-base srt-marker"></div>',
        TPL_RECTANGLE = '<div class="srt-base srt-rectangle"></div>';
        TPL_SHADOW = '<div class="srt-base srt-shadow"></div>'
        TPL_CLOSE = '<div class="srt-base srt-close"></div>';
    var _private = {
        trigger : 0,
        startLeft: 0,
        startTop: 0,
        rectangle: null,
        renderClose: function(left, top) {
            var coords = _private.getCoords(left, top);
            var close = $(TPL_CLOSE).appendTo('body');
            return close
                .css('left', (coords.left + coords.width - Math.round(close.width() / 2)) + 'px')
                .css('top', (coords.top - Math.round(close.height() / 2)) + 'px');
        },
        renderRectangle : function() {
            _private.rectangle = $(TPL_RECTANGLE).appendTo('body');
        },
        renderShadowBox : function(left, top, width, height) {
            return $(TPL_SHADOW).appendTo('body')
                .css('left', left + 'px')
                .css('top', top + 'px')
                .css('width', width + 'px')
                .css('height', height + 'px');
        },
        renderShadow : function() {
            var coords = _private.rectangle.offset();
            coords.width = _private.rectangle.width();
            coords.height = _private.rectangle.height();
            _private.renderShadowBox(0, 0, $(document).width(), coords.top);
            _private.renderShadowBox(0, coords.top + coords.height
                , $(document).width(), ($(document).height() - coords.top - coords.height));
            _private.renderShadowBox(0, coords.top, coords.left, coords.height);
            _private.renderShadowBox(coords.width + coords.left, coords.top
                , ($(document).width() - coords.width - coords.left), coords.height);

        },
        saveCoords : function() {
            var coords = _private.rectangle.offset();
            $('div.srt-feedback form input[name=srt-data]').val(
                coords.left + ',' + coords.top + ',' +
                _private.rectangle.width() + ',' + _private.rectangle.height()
            );
        },
        removeAll : function() {
            $('body .srt-base').remove();
            $(window).unbind('resize.rst');
             _private.trigger = 0;
        },
        getCoords : function(left, top) {
            return {left : (left > _private.startLeft ? _private.startLeft : left),
                width : Math.abs(left - _private.startLeft),
                top : (top > _private.startTop ? _private.startTop : top),
                height : Math.abs(top - _private.startTop)};
        },
        updateRectangle : function(left, top) {
            var coords = _private.getCoords(left, top);
            _private.rectangle
                .css('top', coords.top + 'px')
                .css('left', coords.left + 'px')
                .css('width', coords.width+ 'px')
                .css('height', coords.height + 'px');
        },
        startCapturing : function(e) {
            var marker = $(TPL_MARKER).appendTo('body');
            marker
            .css('top',  (e.pageY - Math.round(marker.height() / 2)) + 'px')
            .css('left', (e.pageX - Math.round(marker.width() / 2)) + 'px')
            .addClass('start');
            _private.startLeft = e.pageX;
            _private.startTop = e.pageY;
            $('body').unbind('mousemove.srt')
            .bind('mousemove.srt', _handler.capturing);
            _private.renderRectangle();
        },
        stopCapturing : function(e) {
            $('body').unbind('mousemove.srt');
             var marker = $(TPL_MARKER).appendTo('body');
            marker
                .css('top', (e.pageY - Math.round(marker.height() / 2)) + 'px')
                .css('left', (e.pageX - Math.round(marker.width() / 2)) + 'px')
                .addClass('end');
            _private.renderShadow();
            $(window).bind('resize.rst', _private.renderShadow);
            _private.renderClose(e.pageX, e.pageY)
                .bind('click.srt', _handler.onClose);
            _private.saveCoords();
        },
        removeTip : function() {
            $('div.srt-tip').remove();
        }
    };
    var _handler = {
       onClose : function(e) {
           e.preventDefault();
           e.stopImmediatePropagation();
            _private.removeAll();
       },
       capturing : function(e) {
            _private.updateRectangle(e.pageX, e.pageY);
       },

       onClick : function(e) {
           _private.removeTip();
           if (_private.trigger > 1)
               return;
           if (_private.trigger) {
               _private.stopCapturing(e);
           } else {
               _private.startCapturing(e);
           }
           _private.trigger ++;
       }
    };
    return {
        start : function() {
            $('body').bind('click.srt', _handler.onClick);
        },
        stop : function() {
            _private.removeAll();
            $('body').unbind('click.srt');
        }
    }
}());

var FeedbackForm =(function() {
    var TPL_TIP = '<div class="srt-tip"><div>'
        + 'Mark up a rectangled area on the page by clicking'
        + '</div></div>',
        TPL_LOCK = '<div class="srt-lock"><!-- --></div>';
    var _node = {};
    var _private = {
        lockScreen : function() {
            _node.lock = $(TPL_LOCK).appendTo(_node.body);
        },
        unlockScreen : function() {
            _node.lock.remove();
        },
        showTip : function() {
            var tip = $(TPL_TIP).appendTo(_node.body);
            setTimeout(function(){
                tip.remove();
            }, 2500);
        },
        startHighlight : function() {
            _node.startHighlight.hide();
            _node.stopHighlight.show();
            _private.lockScreen();
            Highlighting.start();
        },
        stopHighlight : function() {
            _node.startHighlight.show();
            _node.stopHighlight.hide();
            _private.unlockScreen();
            Highlighting.stop();
        }
    };
    var _handler = {
        startHighlight : function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            _private.startHighlight();
        },
        stopHighlight : function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            _private.stopHighlight();
        },
        closeForm : function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            _node.feedbackForm.hide();
        }
    }
    return {
            init : function() {
                _node = _parseNodes({
                    feedbackForm : 'div.srt-feedback',
                    startHighlight : 'div.srt-feedback button.srt-highlight.srt-start',
                    stopHighlight : 'div.srt-feedback button.srt-highlight.srt-stop',
                    body : 'body',
                    closeForm : 'a.srt-close'
                });
                _node.feedbackForm.show();
                _private.startHighlight();
                _private.showTip();
                _node.startHighlight
                    .unbind('click.srt')
                    .bind('click.srt', _handler.startHighlight);
                _node.stopHighlight
                    .unbind('click.srt')
                    .bind('click.srt', _handler.stopHighlight);
                _node.closeForm
                    .unbind('click.srt')
                    .bind('click.srt', _handler.closeForm);
            }
        }
}());

var FeedbackBtn =(function() {
    var _node = [];
     var _handler = {
        showFeedback : function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            FeedbackForm.init();
        }
     };
    return {
            init : function() {
                _node = _parseNodes({
                    feedbackBtn : 'div.srt-feedback-btn'
                });
                _node.feedbackBtn.bind('click.srt', _handler.showFeedback);
            }
        }
}());
// Document is ready
$(document).bind('ready.app', FeedbackBtn.init);

})( jQuery );
