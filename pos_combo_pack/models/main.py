from openerp import api, fields, models


class pos_order_line_combo(models.Model):
    _name = "pos.order.line.combo"
    
    qty = fields.Float('Quantity', default='1', required=True)
    product_id = fields.Many2one('product.product', 'Item')
    line_id = fields.Many2one('pos.order.line', 'POS Line')
    
    
class pos_order_line(models.Model):
    _inherit = "pos.order.line"
    
    is_pack = fields.Boolean("Is Combo Pack")
    combo_ids = fields.One2many("pos.order.line.combo", 'line_id', "Combo Line")
    

class ProductPack(models.Model):
    _name = "product.pack"
    _description = "Product packs"


    product_categ_id = fields.Many2one('pos.category', 'Category')
    product_quantity = fields.Float('Quantity', default='1', required=True)
    product_template_id = fields.Many2one('product.template', 'Item')

class FixProductPack(models.Model):
    _name = "fix.product.pack"


    product_p_id = fields.Many2one('product.product', 'Product')
    product_quantity = fields.Float('Quantity', default='1', required=True)
    product_template_id = fields.Many2one('product.template', 'Item')



class pos_order_line_own(models.Model):
    _name = "pos.order.line.own"
    qty = fields.Float('Quantity', default='1', required=True)
    product_id = fields.Many2one('product.product', 'Item')
    orderline_id = fields.Many2one('pos.order.line', 'POS Line')
    price  = fields.Float('Price',required=True)
    
class pos_order_line(models.Model):
    _inherit = "pos.order.line"
    
    is_extra = fields.Boolean("Is Extra")
    own_ids = fields.One2many("pos.order.line.own", 'orderline_id', "Extra Toppings")
    
class ProductExtraTopping(models.Model):
    _name = "product.extra.topping"
    _rec_name = 'product_categ_id'

    product_template_id = fields.Many2one('product.template', 'Item')
    multi_selection = fields.Boolean("Multiple Selection")
    product_categ_id = fields.Many2one('pos.category', 'Category', required=True)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_pack = fields.Boolean('Combo Pack', default=False)
    is_extra = fields.Boolean('Make Own', default=False,help="This will use for ")
    product_extra_id = fields.One2many('product.extra.topping', 'product_template_id', 'Product Toppings')
    product_pack_id = fields.One2many('product.pack', 'product_template_id', 'Items in the pack')
    product_fix_pro_ids = fields.One2many('fix.product.pack','product_template_id', 'Fix Pack Product')