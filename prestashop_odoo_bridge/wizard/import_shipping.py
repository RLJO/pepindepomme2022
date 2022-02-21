import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api

class ImportPrestashopShipping(models.TransientModel):
    _name = "import.prestashop.shipping"
    _inherit = "import.operation"
    _description = "Import Prestashop Shipping"

    def import_now(self,**kwargs):
        data_list = []
        prestashop = self._context.get("prestashop")
        channel_id = self.channel_id
        if kwargs.get("prestashop_object_id"):
            vals = self.get_shipping_vals(channel_id, prestashop, **kwargs)
            if isinstance(vals,dict):
                data_list.append(vals)
        else:
            data_list = self.get_shipping_all(prestashop, channel_id,**kwargs)
        return data_list

    def get_shipping_all(self,prestashop ,channel_id,**kwargs):
        vals_list = []
        limit = '{},{}'.format(kwargs.get("page"),kwargs.get('page_size"'))
        try:
            shipping_data = prestashop.get("carriers", options={'limit':limit})
            shipping_data = shipping_data.get("carriers")
            if isinstance(shipping_data,str):
                return vals_list
        except Exception as e:
            _logger.info("ShippingError : %r",str(e))
        else:
            shipping_ids = shipping_data.get("carrier")
            if isinstance(shipping_ids,list):
                vals_list = list(map(lambda x: self.get_shipping_vals(
                    channel_id,prestashop,prestashop_object_id = x.get("attrs",{}).get("id")),shipping_ids))
        return vals_list

    def get_shipping_vals(self, channel_id, prestashop, **kwargs):
        try:
            shipping_data = prestashop.get("carriers",kwargs.get("prestashop_object_id"))
        except Exception as e:
            _logger.info("Shipping Error : %r",str(e))
        else:
            return {
                "name": shipping_data["carrier"].get("name"),
                "store_id": shipping_data["carrier"].get("id"),
                "shipping_carrier": shipping_data["carrier"].get("name"),
                "channel_id": channel_id.id,
                "channel": channel_id.channel,
                "description": shipping_data["carrier"].get("description",False)
                }
