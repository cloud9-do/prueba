# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Multi Shop",
  "summary"              :  "This module allows the seller to create multiple shop in POS.",
  "category"             :  "Point of sale",
  "version"              :  "1.5.2",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-POS-Shops.html",
  "description"          :  """https://webkul.com/blog/odoo-pos-multi-shop/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_shops&version=10.0",
  "depends"              :  ['point_of_sale'],
  "data"                 :  [
                             'views/pos_shop_view.xml',
                             'views/template.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo"                 :  ['data/pos_shop_demo.xml'],
  "qweb"                 :  ['static/src/xml/pos_shop.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  149,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}