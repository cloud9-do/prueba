odoo.define('pos_shop.pos_shop', function(require) {
	"use strict";
	var models = require('point_of_sale.models');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var pos_model = require('point_of_sale.models');
	var core = require('web.core');
	var _t = core._t;
	var screens = require('point_of_sale.screens');
	var popup_widget = require('point_of_sale.popups');
	var SuperOrder = models.Order;
	var QWeb = core.qweb;
	var shop_ref_id;

	models.load_models([{
		model: 'pos.shop',
		field: [],
		domain: null,
		loaded: function(self,result) {
			self.all_shops_in_pos = result;
			self.db.all_shops = result;
			shop_ref_id = self.config.shop_ref_id[0];
			result.forEach(function(shop){
				if(shop.id == shop_ref_id){
					self.current_shop = shop;
					return true;
				}
			});
			if(self.current_shop){
				var img = new Image();
				img.onload = function() {
					var ratio = 1;
					var targetwidth = 300;
					var maxheight = 150;
					if( img.width !== targetwidth ){
						ratio = targetwidth / img.width;
					}
					if( img.height * ratio > maxheight ){
						ratio = maxheight / img.height;
					}
					var width  = Math.floor(img.width * ratio);
					var height = Math.floor(img.height * ratio);
					var c = document.createElement('canvas');
						c.width  = width;
						c.height = height;
					var ctx = c.getContext('2d');
						ctx.drawImage(img,0,0, width, height);
					self.shop_logo_base64 = c.toDataURL();
				};
				img.src = window.location.origin + '/web/binary/image?model=pos.shop&field=image&id='+self.current_shop.id;
				models.append_shop_domain();
			}
		},

	},
	{
		model:'pos.shop.promotion',
		field: [],
		domain: function(self){
			if (self.current_shop)
				return [['id','in',self.current_shop.promotion_ids]];
		},
		loaded: function(self,result) {
			self.all_promotion_in_pos = result;
		}

	}],{
			'before': 'pos.category'
		}
	);

	models.append_shop_domain = function() {
		var models_list = models.PosModel.prototype.models;
		for (var i = 0; i < models_list.length; i++) {
			var model = models_list[i];
			if (model.model === "product.product") {
				models_list[i].domain.push(['shop_ids','in',[shop_ref_id]]);
			}
		}
	}
	models.Order = models.Order.extend({
		export_for_printing: function() {
			var self = this;
			var dict = SuperOrder.prototype.export_for_printing.call(this);
			var juan = false;
			if(self.pos.current_shop && juan)
				dict.shopdata = this.get_shop_details();
			return dict;
		},
		get_shop_details: function() {
			var self = this;
			var shop_ref_id = self.pos.config.shop_ref_id[0];
			var shops = self.pos.db.all_shops;
			var website = "";
			var email = "";
			var name = "";
			var phone = "";
			var shop_logo = null;
			var shop_promotions = [];
			var street = "";
			var street2 = "";
			var city = "";
			var state_id = null;
			var zip_code = "";
			var country_id = null;
			if(shops) {
				phone = self.pos.current_shop.phone;
				website = self.pos.current_shop.website;
				email = self.pos.current_shop.email;
				name= self.pos.current_shop.name;
				shop_logo = self.pos.shop_logo_base64;
				shop_promotions = self.pos.all_promotion_in_pos;
				street = self.pos.current_shop.street;
				street2 = self.pos.current_shop.street2;
				city = self.pos.current_shop.city;
				zip_code = self.pos.current_shop.zip_code;
				country_id = self.pos.current_shop.country_id;
				state_id = self.pos.current_shop.state_id;

			}
			return {
				email :email,
				website :website,
				name : name,
				phone : phone,
				shop_logo : shop_logo,
				shop_promotions : shop_promotions,
				logo_image : self.pos.current_shop.image,
				street : street,
				street2 : street2,
				city : city,
				zip_code :zip_code,
				country_id :country_id,
				state_id : state_id,

			}

		}
	});
	screens.ReceiptScreenWidget.include({

		print_xml: function() {
			var self = this;
			if(self.pos.current_shop){
				var env = {
					widget:  this,
					pos:	 this.pos,
					order:   this.pos.get_order(),
					receipt: this.pos.get_order().export_for_printing(),
					paymentlines: this.pos.get_order().get_paymentlines()
				};
				var receipt = QWeb.render('WkXmlReceipt',env);
				this.pos.proxy.print_receipt(receipt);
				this.pos.get_order()._printed = true;
			}
			else
				self._super();
		},
	});
});
