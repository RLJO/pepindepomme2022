odoo.define('@website_sale_delivery_colissimo/js/website_sale_delivery_colissimo', async function(require) {
    'use strict';
    let __exports = {};
    /** @odoo-module **/

    var publicWidget = require('web.public.widget');
    require('website_sale_delivery.checkout');
    const {
        qweb: QWeb
    } = require("web.core");

    const WebsiteSaleDeliveryWidget = publicWidget.registry.websiteSaleDelivery;

    // temporary for OnNoResultReturned bug
    //const {registry} = require("@web/core/registry");
    //const {UncaughtCorsError} = require("@web/core/errors/error_service");
    //const errorHandlerRegistry = registry.category("error_handlers");

    //function corsIgnoredErrorHandler(env, error) {
    //    if (error instanceof UncaughtCorsError) {
    //        return true;
    //    }
    //}

    WebsiteSaleDeliveryWidget.include({
        xmlDependencies: (WebsiteSaleDeliveryWidget.prototype.xmlDependencies || []).concat([
            '/website_sale_delivery_colissimo/static/src/xml/website_sale_delivery_colissimo.xml',
        ]),
        events: _.extend({
            "click #btn_confirm_relay": "_onClickBtnConfirmRelay",
        }, WebsiteSaleDeliveryWidget.prototype.events),

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Loads Colissimo the first time, else show it.
         *
         * @override
         */

        _handleCarrierUpdateResult: function(result) {
                var this_ = this
                this._super(...arguments);
                if (result.additionnal_data_colissimo) {

                    $("div[is_colissimo='True']").click(function() {
                        if (!$('#modal_colissimo').length) {
                            this_._loadColissimoModal(result);
                            this_.$modal_colissimo.find('#btn_confirm_relay').on('click', this_._onClickBtnConfirmRelay.bind(this_));
                        } else {
                            this_.$modal_colissimo.modal('show');
                        }
                    });
                }
            }

            ,
        /**
         * This method render the modal, and inject it in dom with the Modial Relay Widgets script.
         * Once script loaded, it initialize the widget pre-configured with the information of result
         *
         * @private
         *
         * @param {Object} result: dict returned by call of _update_website_sale_delivery_return (python)
         */
        _loadColissimoModal: function(result) {
            // add modal to body and bind 'save' button
            $(QWeb.render('website_sale_delivery_colissimo', {})).appendTo('body');
            this.$modal_colissimo = $('#modal_colissimo');
            this.$modal_colissimo.find('#btn_confirm_relay').on('click', this._onClickBtnConfirmRelay.bind(this));

            // load Colissimo script
            const script = document.createElement('script');
            script.src = "/website_sale_delivery_colissimo/static/src/js/jquery.plugin.colissimo.js";

            script.onload = () => {
                // instanciate Colissimo widget
                const params = result.additionnal_data_colissimo
                this.$modal_colissimo.find('#o_zone_widget').frameColissimoOpen(params);
                this.$modal_colissimo.modal('show');
                this.$modal_colissimo.find('#o_zone_widget').trigger("CLS_RebindMap");
            };
            document.body.appendChild(script);

        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------


        /**
         * Update the shipping address on the order and refresh the UI.
         *
         * @private
         *
         */
        _onClickBtnConfirmRelay: function() {
            if (!Colissimo_lastRelaySelected) {
                return;
            }
            this._rpc({
                route: '/website_sale_delivery_colissimo/update_shipping',
                params: {
                    Colissimo_lastRelaySelected,
                },
            }).then((o) => {
                var adress = o["full_adress"]
                $("span[data-oe-expression='order.partner_shipping_id']").html(adress)
                this.$modal_colissimo.modal('hide');
            });
        },
    });

    return __exports;
});;