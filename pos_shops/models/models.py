# -*- coding: utf-8 -*-
#################################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import Warning, ValidationError

class PosShop(models.Model):
	_name = 'pos.shop'

	name = fields.Char(string="Name", ondelete="cascade", translate=True,required=1)
	product_ids = fields.Many2many('product.template',string="Products in Shop", domain=[('sale_ok','=',True),('available_in_pos','=',True)] )
	pos_config_id = fields.Many2one('pos.config',string="Point of Sale",compute="_get_config_details")
	location_id = fields.Many2one('stock.location',string="Stock Location",compute="_get_config_details")
	image = fields.Binary("Image", help="This field holds the image used as avatar for this shop, limited to 1024x1024px")
	related_partner_id = fields.Many2one("res.partner", string="Related Owner")
	state_id = fields.Many2one("res.country.state", related='related_partner_id.state_id', string="State")
	country_id = fields.Many2one("res.country", related='related_partner_id.country_id', string="Country")
	street = fields.Char(related='related_partner_id.street', string="Street")
	street2 = fields.Char(related='related_partner_id.street2', string="Street 2")
	zip_code = fields.Char(related='related_partner_id.zip', string="Zip")
	city = fields.Char(related='related_partner_id.city', string="City")
	website = fields.Char(related='related_partner_id.website', string="Website")
	phone = fields.Char(related='related_partner_id.phone', string="Phone")
	fax = fields.Char(related='related_partner_id.fax', string="Fax")
	email = fields.Char(related='related_partner_id.email', string="Email")
	related_picking_type_id = fields.Many2one("stock.picking.type",compute="_get_config_details" , string="Related Picking Type")
	area = fields.Float(string="Area", help="Shop area in square feet(s).")
	promotion_ids = fields.Many2many('pos.shop.promotion',string="Promotion")

	@api.onchange('related_partner_id')
	def set_shop_image(self):
		if self.related_partner_id.image:
			self.image = self.related_partner_id.image

	@api.one
	def _get_config_details(self):
		for self_obj in self:
			config_ids = self.env['pos.config'].search([('shop_ref_id','=',self_obj.id)])
		if config_ids:
			self.pos_config_id = config_ids[0]
			self.location_id = config_ids[0].stock_location_id 
			self.related_picking_type_id = config_ids[0].picking_type_id

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	available_in_shops = fields.Selection([('all','All'),('specific','Specific')], string="Available in Shops")
	shop_ids = fields.Many2many('pos.shop',string="Shops")

class ProductProduct(models.Model):
	_inherit = 'product.product'

	@api.onchange('available_in_shops')
	def get_availability(self):
		shop_ids = self.shop_ids.search([])		
		if self.available_in_shops == 'all':
			self.shop_ids = shop_ids
		elif not self.available_in_shops:
			self.shop_ids = None
		
	
	@api.onchange('shop_ids')
	def change_shop_ids(self):
		shop_ids = self.shop_ids.search([])	
		if self.shop_ids and len(self.shop_ids) == len(shop_ids):
			self.available_in_shops = 'all'
		elif len(self.shop_ids):
			self.available_in_shops = 'specific'
		else:
			self.available_in_shops = None
	
	@api.constrains('available_in_shops')
	def available_in_shop_contrains(self):
		if self.available_in_shops == 'specific':
			if not self.shop_ids:
				raise ValidationError("Please select atleast one shop")

class PosConfig(models.Model):
	_inherit = 'pos.config'

	shop_ref_id = fields.Many2one('pos.shop',string="Shop")

class PosShopPromotion(models.Model):
	_name = "pos.shop.promotion"

	name = fields.Char(string="Promotion",required=True)
	description = fields.Text('Description',required=True)

