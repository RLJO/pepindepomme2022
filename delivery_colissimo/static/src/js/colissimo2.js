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
                script.src = "https://ws.colissimo.fr/widget-point-retrait/resources/js/jquery.plugin.colissimo.js";
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
            Target: "", // required but handled by OnParcelShopSelected
            Brand: this.recordData.colissimo_brand,
            ColLivMod: this.recordData.colissimo_colLivMod,
            AllowedCountries: this.recordData.colissimo_allowed_countries,
            PostCode: this.recordData.shipping_zip || '',
            Country: this.recordData.shipping_country_code  || '',
            Responsive: true,
            ShowResultsOnMap: true,
            AutoSelect: this.recordData.colissimo_last_selected_id,
            OnParcelShopSelected: (RelaySelected) => {
                const values = JSON.stringify({
                    'id': RelaySelected.ID,
                    'name': RelaySelected.Nom,
                    'street': RelaySelected.Adresse1,
                    'street2': RelaySelected.Adresse2,
                    'zip': RelaySelected.CP,
                    'city': RelaySelected.Ville,
                    'country': RelaySelected.Pays,
                });
                this._setValue(values);
            },
            OnNoResultReturned: () => {
                // HACK while Colissimo fix his bug
                // disable corsErrorHandler for 10 seconds
                // If code postal not valid, it will crash with Cors Error:
                // Cannot read property 'on' of undefined at u.CLS_FitBounds
                const randInt = Math.floor(Math.random() * 100);
//                errorHandlerRegistry.add("corsIgnoredErrorHandler" + randInt, corsIgnoredErrorHandler, {sequence: 10});
//                setTimeout(function () {
//                    errorHandlerRegistry.remove("corsIgnoredErrorHandler" + randInt);
//                }, 10000);
               alert("errrrrrororoororor")
            },
        };
        prompt(JSON.stringify( params))
        this.$el.show();
        //this.$el.MR_ParcelShopPicker(params);
        this.$el.trigger("CLS_RebindMap");


        //codeamiune


$('.o_zone_widget').frameColissimoOpen({
"ceLang" : "fr",
//"callBackFrame" : ‘callBackFrame’,
"URLColissimo" : " https://ws.colissimo.fr",
"ceCountryList" : "FR,ES,GB,PT,DE",
"ceCountry" : "FR",
"dyPreparationTime" : "1",
"ceAddress" : "62 RUE CAMILLE DESMOULINS",
"ceZipCode" : "92130",
"ceTown" : "ISSY LES MOULINEAUX",
"token" :  "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0YWUwYTNlY2M3NzczZDFkMTVlMDYzYjUwMDlhYWQzOSIsImlhdCI6MTY0MTEzMjEzMCwic3ViIjoid2lkZ2V0IiwiaXNzIjoiODAxODA4IiwiZXhwIjoxNjQxMTMzOTMwfQ.SrGZ1Rmo1qeuFwx2xfSo7mRC9FL9QfomEDrNnSt4T6A"
});






        alert("code 2333333333333 ici")
        //codeamine


    },

});

fieldRegistry.add("colissimo_relay", ColissimoWidget);

return __exports;
});
;