/*******************************************************************
*  Filepath: /delivery_colissimo/static/src/js/colissimo.js  *
*  Bundle: web.assets_backend                                      *
*  Lines: 97                                                       *
*******************************************************************/
odoo.define('@delivery_colissimo/js/colissimo', async function (require) {
'use strict';
let __exports = {};
/** @odoo-module **/

const AbstractField = require('web.AbstractField');
const fieldRegistry = require('web.field_registry');


const utils = require('web.utils');
const {qweb, _t} = require('web.core');

// temporary for OnNoResultReturned bug
//const {registry} = require("@web/core/registry");
//const {UncaughtCorsError} = require("@web/core/errors/error_service");
//const errorHandlerRegistry = registry.category("error_handlers");

//function corsIgnoredErrorHandler(env, error) {
//    if (error instanceof UncaughtCorsError) {
//        return true;
//    }
//}


var ColissimoWidget = AbstractField.extend({
    resetOnAnyFieldChange: true,
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */


    _render: function () {
        if (this.recordData.is_colissimo) {
            if (!this.colissimoInitialized) {
                const script = document.createElement('script');
                script.src = "http://localhost/delivery_colissimo/static/src/js/jquery.plugin.colissimo.js";

                script.onload = () => {
                    this.colissimoInitialized = true;
                    this._loadWidget();
                };
                document.body.appendChild(script);
            } else {
                this._loadWidget();
            }
        } else {
            this.$el.hide();
        }
    },

   /**
     *
     * @private
     */



    _loadWidget: function () {


        const params = {
"ceLang" : "fr",
"callBackFrame" : "callBackFrame"  ,
"URLColissimo" : " https://ws.colissimo.fr",
"ceCountryList" : "FR,ES,GB,PT,DE",
"ceCountry" : "FR",
"dyPreparationTime" : "1",
"ceAddress" : this.recordData.colissimo_ceAddress,
"ceZipCode" : this.recordData.shipping_zip,
"ceTown" : this.recordData.colissimo_ceTown,
"token" :  this.recordData.colissimo_ceToken
};

        this.$el.show();
        //this.$el.MR_ParcelShopPicker(params);
        $('.o_zone_widget').frameColissimoOpen(params);
        this.$el.trigger("CLS_RebindMap");
    },

});

fieldRegistry.add("colissimo_relay", ColissimoWidget);

return __exports;
});
;