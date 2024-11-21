/*globals define, WebGMEGlobal*/

/**
 * Generated by VisualizerGenerator 1.7.0 from webgme on Wed Nov 20 2024 22:43:40 GMT-0600 (Central Standard Time).
 */

define(['css!./styles/SmToSVGWidget.css'], function () {
    'use strict';

    var WIDGET_CLASS = 'sm-to-s-v-g';

    function SmToSVGWidget(logger, container) {
        this._logger = logger.fork('Widget');

        this._el = container;

        this.nodes = {};
        this._initialize();

        this._logger.debug('ctor finished');
    }

    SmToSVGWidget.prototype._initialize = function () {
        var width = this._el.width(),
            height = this._el.height(),
            self = this;

        // set widget class
        this._el.addClass(WIDGET_CLASS);
        this._iframe = null;

    };

    SmToSVGWidget.prototype.onWidgetContainerResize = function (width, height) {
        this._logger.debug('Widget is resizing...');
    };

    SmToSVGWidget.prototype.initNode = function (hash, path) {
        var iframe = document.createElement('iframe');
        iframe.name = "SmSVG";
        iframe.style.height = "100%";
        iframe.style.width = "100%";
        iframe.src = '/extlib/src/common/svg/' + hash.replace('#','_') + '_' + path.replace('/','_') + '.svg';
        
        this._el.append(iframe);
        this._iframe = iframe;
    };

    SmToSVGWidget.prototype.refresh = function () {
        this._iframe.contentWindow.location.reload(true);
    }

    /* * * * * * * * Visualizer life cycle callbacks * * * * * * * */
    SmToSVGWidget.prototype.destroy = function () {
    };

    SmToSVGWidget.prototype.onActivate = function () {
        this._logger.debug('SmToSVGWidget has been activated');
    };

    SmToSVGWidget.prototype.onDeactivate = function () {
        this._logger.debug('SmToSVGWidget has been deactivated');
    };

    return SmToSVGWidget;
});