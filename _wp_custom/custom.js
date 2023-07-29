var _iub = _iub || [];

jQuery(document).ready(function ($) {
	
	//Sticky Header
	jQuery(".tm-header").addClass("uk-sticky");
	jQuery(".tm-header").attr("uk-sticky","");
	
	// NAVBAR MOBILE
	//$('#tm-dialog-mobile').addClass("uk-light");
	
	$('#account-icon-light').parent().replaceWith('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><g id="account-icon-dark" transform="translate(-184 -2042)"><rect id="Rettangolo_34" data-name="Rettangolo 34" width="32" height="32" rx="8" transform="translate(184 2042)" fill="#e8e8e8" opacity="0.301"/><path id="Path_12_1_" d="M220.718,437.14c0-3.015-2.378-5.606-5.818-6.54" transform="translate(-11.113 1628.95)" fill="none" stroke="#292b32" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5"/><path id="Path_13_1_" d="M169.494,431.1c-3.122.934-5.394,3.525-5.394,6.434" transform="translate(27.9 1628.556)" fill="none" stroke="#292b32" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5"/><circle id="Ellipse_5_1_" cx="5.181" cy="5.181" r="5.181" transform="translate(195.5 2049.909)" fill="none" stroke="#292b32" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5"/></g></svg>');
	
	$('#cart-icon-light').parent().replaceWith('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><g id="cart-icon-dark" transform="translate(-795.742 -1650.107)"><rect id="Rettangolo_34" data-name="Rettangolo 34" width="32" height="32" rx="8" transform="translate(795.742 1650.107)" fill="#e8e8e8" opacity="0.301"/><path id="Tracciato_65" data-name="Tracciato 65" d="M-64.927,275.033h-3.458a2.169,2.169,0,0,1-.994,2.73,2.124,2.124,0,0,1-2.427-.233A2.186,2.186,0,0,1-72.416,275a2.084,2.084,0,0,1-1.632-1.881,2.061,2.061,0,0,1,1.231-2.134,23.466,23.466,0,0,1-1.113-4c-.419-1.631-.779-3.276-1.165-4.915a1.751,1.751,0,0,0-1.768-1.4c-.272,0,.2,0-.073,0a.676.676,0,0,1-.7-.668.664.664,0,0,1,.683-.679,3.165,3.165,0,0,1,3.194,2.5c.085.365.168.731.256,1.116.057-.042.1-.067.133-.1a2.745,2.745,0,0,1,1.807-.656q4.478,0,8.957,0a2.769,2.769,0,0,1,2.707,3.435q-.533,2.232-1.1,4.456a2.735,2.735,0,0,1-2.673,2.078q-4.1.006-8.2,0a.817.817,0,0,0-.663.267.747.747,0,0,0,.395,1.216,1.522,1.522,0,0,0,.331.028l8.79,0a2.21,2.21,0,0,1,2.218,1.742,2.178,2.178,0,0,1-1.64,2.563,2.176,2.176,0,0,1-2.608-1.669A2.27,2.27,0,0,1-64.927,275.033Zm-2.166-11.478c-1.5,0-2.992,0-4.487,0a1.4,1.4,0,0,0-1.38,1.747q.515,2.141,1.042,4.279a1.428,1.428,0,0,0,1.58,1.225h4.024c.853,0,1.706.005,2.559,0a1.388,1.388,0,0,0,1.432-1.126q.536-2.155,1.062-4.312a1.409,1.409,0,0,0-1.437-1.812Zm5.005,12.293a.821.821,0,0,0-.83-.815.824.824,0,0,0-.819.826.836.836,0,0,0,.831.82A.832.832,0,0,0-62.088,275.848Zm-7.508.014a.813.813,0,0,0-.811-.829.815.815,0,0,0-.829.812.827.827,0,0,0,.812.834A.824.824,0,0,0-69.6,275.862Z" transform="translate(879.709 1397.437)" fill="#282b33"/></g></svg>')
	
	//
	//Button icon
    $(".uk-button-default, .uk-button-primary, .uk-button-secondary").prepend('<svg width="24" height="24" viewBox="0 0 24 24"><g transform="translate(-2046 -697)"><circle id="ellisse" cx="12" cy="12" r="12" transform="translate(2046 697)" fill="#fff"/><g id="chevron" transform="translate(1945 2333.548) rotate(-90)"><line id="linea-bottom" x2="3.524" y2="4" transform="translate(1620.5 111.5)" fill="none" stroke="#000" stroke-linecap="round" stroke-width="1.5"/><line id="linea-top" x1="3.524" y2="4" transform="translate(1623.976 111.5)" fill="none" stroke="#000" stroke-linecap="round" stroke-width="1.5"/></g></g></svg>');
	
	$(".uk-button-default").hover(function(){
		TweenMax.to('.uk-button-default svg', {scale: .9, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-default #chevron', {opacity: 1, ease: Power4.easeInOut});
	}, function(){
		TweenMax.to('.uk-button-default svg', {scale: .4, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-default #chevron', {opacity: 0, ease: Power4.easeInOut});
	});
	
	$(".uk-button-primary").hover(function(){
		TweenMax.to('.uk-button-primary svg', {scale: .9, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-primary #chevron', {opacity: 1, ease: Power4.easeInOut});
	}, function(){
		TweenMax.to('.uk-button-default svg', {scale: .4, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-default #chevron', {opacity: 0, ease: Power4.easeInOut});
	});
	
	$(".uk-button-secondary").hover(function(){
		TweenMax.to('.uk-button-secondary svg', {scale: .9, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-secondary #chevron', {opacity: 1, ease: Power4.easeInOut});
	}, function(){
		TweenMax.to('.uk-button-secondary svg', {scale: .4, ease: Power4.easeInOut});
		TweenMax.to('.uk-button-secondary #chevron', {opacity: 0, ease: Power4.easeInOut});
	});
	
	//HOME PINNED SECTIONS
	//

	/*
	
	gsap.registerPlugin(ScrollTrigger);
	
	
	let mm = gsap.matchMedia();

	mm.add("(min-width: 800px)", () => {
	
		ScrollTrigger.create({
			trigger: "#astucci-gioielli",
			start: "top top", 
			end: "bottom bottom",
			pin: "#ag-img",
			markers: true
		});

	});
	
	*/

	// CARD PRODOTTO
	
	// IF HOME

	var products = $('li.product');
	var productsTitle = $(products).find('h2');
	var productsPrice = $(products).find('span.price');
	var productsImage = $(products).find('.woocommerce-loop-product__link');
	var productsAddToCart = $(products).find('.product_type_variable');

	for (const title of productsTitle) {
		$(title).insertBefore($(title).parent());
	}

	for (const price of productsPrice) {
		$(price).insertBefore($(price).parent());
	}

	for (var x = 0; x < productsImage.length; x++) {

		$(productsImage[x]).add($(productsAddToCart[x])).wrapAll('<div class="product-media-top"></div>')

	}
	
	check = true;
	
	setInterval(()=>{
		
		var cl_products = $('div.cl-layout__item');
		var cl_productsImage = $(cl_products).find('.cl-element-featured_media__anchor');
		var cl_productsAddToCart = $(cl_products).find('.hover-button');

		for (var i = 0; i < cl_products.length; i++) {

			$(cl_productsAddToCart[i]).appendTo($(cl_productsImage[i]));
		}	
	
	},1000)
/*
	var cl_products = $('div.cl-layout__item');
	var cl_productsImage = $(cl_products).find('.cl-element-featured_media__anchor');
	var cl_productsAddToCart = $(cl_products).find('.hover-button');
	
	for (var i = 0; i < cl_products.length; i++) {
		
		$(cl_productsAddToCart[i]).appendTo($(cl_productsImage[i]));
	}
*/
	
	/*
	for (var x = 0; x < cl_productsImage.length; x++) {

		$(cl_productsImage[x]).add($(cl_productsAddToCart[x])).wrapAll('<div class="product-media-top"></div>')

	}
	*/
	for (const product of products) {

		$(product).prepend($(product).find('.product-media-top'));
	}

	// PAGINA SHOP
	/*
    if ($('#af-archive')) {
        // CUSTOMIZE SEARCH & FILTER
        $('#search-filter-form-1596 > ul > li.sf-field-search').prepend('<h4 class="uk-hidden"></h4>');
        $('#search-filter-form-1596 > ul').attr('uk-accordion', 'collapsible: true; multiple: true;');
        $('#search-filter-form-1596 > ul > li').addClass('el-item').addClass('uk-open');
        $('#search-filter-form-1596 > ul > li > h4').addClass('uk-accordion-title');
        $('#search-filter-form-1596 > ul > li > ul').addClass('uk-accordion-content');
    }
	*/
	// SEARCH AND FILTER
	
	if ($('body').hasClass('archive')) {
		
		$('.sf-input-text').addClass('uk-input');
		$('.sf-input-select').addClass('uk-select');
//		$('.sf-input-checkbox').addClass('uk-checkbox');
		$('.sf-field-reset a').prepend('<span uk-icon="icon: refresh; ratio: 1.2;" style="margin-right: 8px;"></span>');
		
		if ($('html').attr('lang') == 'en-US') { 
			$('#modal-full .sf-field-reset').append('<a id="apply-button"><span uk-icon="icon: check; ratio: 1.2;" style="margin-right: 8px;"></span>Apply</a>');
		} else {
			$('#modal-full .sf-field-reset').append('<a id="apply-button"><span uk-icon="icon: check; ratio: 1.2;" style="margin-right: 8px;"></span>Applica</a>');
		}
		
		$('#modal-full .sf-field-reset').on('click', '#apply-button', function() {
			$('button.uk-close').click();
			
			$([document.documentElement, document.body]).animate({
				scrollTop: $("#product-filters-mobile").offset().top
			}, 200);
			
		});
		
		// aggiungere spazio a colori specifici
		var colors = $('li.sf-field-taxonomy-colore ul li label.sf-label-checkbox');
		console.log(colors);
		
		for (const color of colors) {
			var labelText = $(color).clone().children().remove().end().text().trim();
			
			switch (true) {
				case (labelText == "BLUMARINE"):
					labelText = "BLU MARINE";
					break;
				case (labelText == "COLORESTANDARD"):
					labelText = "COLORE STANDARD";
					break;
				case (labelText == "MARRONEAVORIO"):
					labelText = "MARRONE - AVORIO";
					break;
				case (labelText == "PLATINO(EXMARRONE)"):
					labelText = "PLATINO (EX MARRONE)";
					break;
				case (labelText == "ROSSOROSSO"):
					labelText = "ROSSO - ROSSO";
					break;
			}
			$(color).text(labelText);
			console.log(labelText);
		}
	}
	
	// PAGINE SHOP / CATEGORIA
	/*
	if ($('body').hasClass('archive')) {
		
		$('body > div.tm-page > div.uk-section-default.uk-section.uk-section-large > div > div'). append($('.cl-pagination'));
		$('.cl-pagination').addClass('uk-text-center').addClass('uk-margin-large');
		
	}
	*/
	
	// PAGINA PRODOTTO SINGOLO
	// 
	
	// IF SINGLE PRODUCT
	
    if ($('body').hasClass('single-product')) {

        $('table.variations').addClass('uk-table').addClass('uk-table-middle');

        var table = $('table.variations>tbody');
        var rows = $(table).find('tr');

        // console.log(rows);

        // $(table).append('<tr class="nuova"><tr>');
        for (var n = 0; n < rows.length; n++) {
            $(rows[n]).addClass('' + n);
        }

        $('th.label, td.value').css('display', 'table-cell');

        $('tr.1').insertBefore("tr.0");

        $(table).append('<tr class="custom-row0"></tr>');
        $('<tr class="custom-row1"></tr>').insertAfter('tr.1');

        $('tr.0').append('<th class="label quantity"><label>Quantità</label></th>');
        $('tr.custom-row0').append($('tr.0>td'));
        $('tr.custom-row0').append($('<td class="moved-quantity"></td>'));

        $('td.moved-quantity').append($('div.quantity'));

        $('tr.1').append('<th></th>');
        $('tr.custom-row1').append($('tr.1>td'));
        $('tr.custom-row1').append($('<td></td>'));

        $('tr.1 th.label').attr('colspan', '2');
        $('tr.custom-row1 td.value').attr('colspan', '2');

        $('tr.custom-row0 td.value').css('width', '70%');
        $('td.moved-quantity').css('margin-left', '24px');
        $('th.label.quantity').css('margin-left', '24px');
        $('div.quantity').css('width', '100%');
		if ($('html').attr('lang') == 'en-US') { 
			$('th.quantity>label').text('Quantity');
			
			$('.vpc-configure-button').text('Customize cliché')
		}
        $('div.quantity>input').css('width', '100%');

        $('a.reset_variations').insertAfter('#pa_dimensione');
		
		// ADD TO CART
		// 
		//console.log(JSON.parse($('form.variations_form').attr('data-product_variations')));
		
		
		// rimuove eventuali configure button duplicati
		var found = {};
		$('.vpc-configure-button').each(function(){
			var $this = $(this);
			if(found[$this.data('id')]){
				 $this.remove();   
			}
			else{
				 found[$this.data('id')] = true;   
			}
		});

        // hide default add to cart button
        $('.single_add_to_cart_button').css('display', 'none');
        // append configure button to sticky container
        $('#sticky-add-to-cart').prepend($('.vpc-configure-button'));
		// hide custom table
		$('table.custom-variation').addClass('hide-table');
		// hide custom buttons
        $('.vpc-configure-button').addClass('hide-button');
        $('#custom-add-to-cart').addClass('hide-button');
        $('#custom-add-to-cart').css('margin-left', '20px');
		
		// on form change show custom table
		$('form.variations_form.cart').on('change', function() {
			
			if ($('#pa_colore').val() != '' && $('#pa_dimensione').val() != '') {
				$('table.custom-variation').removeClass('hide-table');				
			} else {
				$('table.custom-variation').addClass('hide-table');
			}
			
		})
		
		$('#customize').on('change', () => {
			if ($('#customize').val() == 'yes') {
				// show VPC configure button
				$('.vpc-configure-button').removeClass('hide-button');
				var vpc = $('.vpc-configure-button[style*="display: inline"]');
				vpc.css('display', 'inline-block');
				console.log(vpc);
		        $('#custom-add-to-cart').addClass('hide-button');
			} else if ($('#customize').val() == 'no') {
				// show add to cart
				$('.vpc-configure-button').addClass('hide-button');
		        $('#custom-add-to-cart').removeClass('hide-button');
			} else {
				$('.vpc-configure-button').addClass('hide-button');
       			$('#custom-add-to-cart').addClass('hide-button');
			}
		});
		
        // on click custom add to cart submit form
        $('#custom-add-to-cart').on('click', () => {
            $('.single_add_to_cart_button').click();
        });
		
		$('.vpc-configure-button').on('click', function(e) {
			e.preventDefault();
      var id = $(this).attr("id")
      var confNumber = id.split('-').pop() // Last part of the id is the configurator's number
			var inputQuantity = $('input.qty').val();
			var href = $(this).attr('href');
			var hrefWithQty = href+'configure/'+confNumber+'/?qty='+inputQuantity
      window.location.href= hrefWithQty
      console.log(hrefWithQty)
		})
		
		// $('.woocommerce-Price-currencySymbol').css('display', 'none');
		
		// $('span.woocommerce-Price-amount').prepend($('span.woocommerce-Price-currencySymbol'));
		
    }
	
	// CONFIGURATORE

  // desired url example
  // https://arturofacchini.it/en/configurator/configure/8303/?qty=12

	if ($('body').hasClass('page-id-78') || $('body').hasClass('page-id-293')) {
		
		var colors = $('.vpc-single-option-wrap');
		
		for (const color of colors) {
			
				if ($(color).find('input')) {
					var parent = $(color).find('input').parent();
					if (!parent.hasClass('custom-uploader')) {
						var value = $(color).find('input').val();
						$(color).append(value);
						$(color).css({
							"font-size":"14px",
							"display":"flex",
							"align-items":"center"
						});
						
					}
				}
			
		}
		
		$('#vpc-components').prepend($('.conf_desc'));
		
		$('#vpc-components').prepend($('h1'));
		
		$('#vpc-price-container').remove();
		$('.vpc-selected-icon').remove();
		$('.vpc-group-name').remove();
		
		$('#vpc-components').append($('.vpc-action-buttons'));
		
		$('#vpc-preview-wrap').prepend($('#mva-bx-pager'));

		
		$('#vpc-components > div[data-component-focus="fronte"]').css('display', 'block');
		$('#vpc-components > div[data-component-focus="retro"]').css('display', 'none');
		$('#vpc-components > div[data-component-focus="front"]').css('display', 'block');
		$('#vpc-components > div[data-component-focus="back"]').css('display', 'none');
		$('#vpc-components > div[data-component-focus="interno"]').css('display', 'block');
		$('#vpc-components > div[data-component-focus="esterno"]').css('display', 'none');
		$('#vpc-components > div[data-component-focus="inside"]').css('display', 'block');
		$('#vpc-components > div[data-component-focus="outside"]').css('display', 'none');
		
		$('.bx-pager-item a').on('click', function() {
			//console.log($(this).attr('data-slide-index'));
			
			var index = $(this).attr('data-slide-index');
			
			if (index == 0) {
				$('#vpc-components > div[data-component-focus="front"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="back"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="fronte"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="retro"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="interno"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="esterno"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="inside"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="outside"]').css('display', 'none');
			} else {
				$('#vpc-components > div[data-component-focus="front"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="back"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="fronte"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="retro"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="interno"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="esterno"]').css('display', 'block');
				$('#vpc-components > div[data-component-focus="inside"]').css('display', 'none');
				$('#vpc-components > div[data-component-focus="outside"]').css('display', 'block');
			}
		});
		
	}
	
	
	// REGISTRATION FORM
	
	/*
	function verificaPIVA(piva) {
		var valid = false;
		if (/^[0-9]{11}$/.test(piva)) {
			var s = 0;
			for (var i = 0; i <= 9; i += 2) s += parseInt(piva.charAt(i));
			for (var i = 1; i <= 9; i += 2) {
				var c = 2 * parseInt(piva.charAt(i));
				if (c > 9) c = c - 9;
				s += c;
			}
			var c = (10 - s % 10) % 10;
			if (c == parseInt(piva.charAt(10))) {
				valid = true;
			}
		}
		return valid;
	}
	
	$('span.wpcf7-not-valid-piva').css('display', 'none');
	
	// Aggiunge un listener all'evento blur del campo di input
	$('#partita-iva').on('blur', function() {
		var piva = $(this).val();
		var valid = verificaPIVA(piva);
		if (valid) {
			$('span.wpcf7-not-valid-piva').css('display', 'none');
			$('#submit-form input').prop('disabled', false);
			$(this).removeClass('wpcf7-not-valid');
		} else {
			$('span.wpcf7-not-valid-piva').css('display', 'block');
			$(this).addClass('wpcf7-not-valid');
			$('#submit-form input').prop('disabled', true);
		}
	});
	*/
	// fill fullname field
	if ($('#registration-form')) {
		
		$('#first-name, #last-name').on('input',function(e){
			
			$('#full-name').val($('#first-name').val().trim() + ' ' + $('#last-name').val().trim());
		});

	}
	
	// SLIDESHOW MEGA MENU GIOIELLI 
	/*
	if ($('.tm-header nav.uk-navbar')) {
		
		var gioielliNavItems = $('#nav-gioielli ul li a');
		
		$(gioielliNavItems).hover(function(e) {
			
			UIkit.slideshow($('#astucci-gioielli'), 0).show($(gioielliNavItems).index(this));
		});
		
		var espositoriNavItems = $('#nav-espositori ul li a');
		
		$(espositoriNavItems).hover(function(e) {
			
			UIkit.slideshow($('#espositori-gioielli'), 0).show($(espositoriNavItems).index(this));
		});
	}
	*/
	// ACCOUNT PAGE
	if ($('#account-section')) {
		var accountSection = $('#account-section');
		if ($('body').hasClass('logged-in')) {
			jQuery("#account-section").css('background-image', 'none');
		}
	}
		// aggiungi link immagine alla vista ordine
	if ($('body').hasClass('woocommerce-view-order')) {
		var images = $('.uploaded_image');
		
		for (const image of images) {
			var src = $(image).find('img').attr('src');
			$(image).find('img').wrapAll('<a target="_blank" href="'+src+'"></a>');
		}
	} 
	
	// CARRELLO DIALOG
	if ( $('#nav_menu-4 > ul > li:nth-child(2) > a') ) {
		var carrello = $('#nav_menu-4 > ul > li:nth-child(2) > a');
		carrello.attr('href', '#tm-dialog');
		carrello.attr('uk-toggle', '');
		var counter = carrello.find('span');
		//console.log(counter[0]);
		if ($(counter[0]).text() == "") {
			$(counter[0]).remove();
		} else {
			
			var number = $(counter[0]).text();
			var result = number.substring(1, number.length-1);
			$(counter[0]).remove();
			carrello.append('<span class="menu-cart">'+result+'</span>');
		}
		
	}
	
	// CARRELLO MOBILE
	if ($('body > div.tm-page > div.tm-header-mobile > div.uk-sticky > div > div > nav > div.uk-navbar-right > ul > li > a')) {
		var mobileCart = $('body > div.tm-page > div.tm-header-mobile > div.uk-sticky > div > div > nav > div.uk-navbar-right > ul > li:nth-child(2) > a');
		var mobileMenuCart = $('#nav_menu-12 > ul > li:nth-child(2) > a');
		
		var mobileCounter = mobileCart.find('span');
		var mobileMenuCounter = mobileMenuCart.find('span');
		
		if ($(mobileCounter[0]).text() == "") {
			$(mobileCounter[0]).remove();
		} else {
			
			var mobileNumber = $(mobileCounter[0]).text();
			var mobileResult = mobileNumber.substring(1, mobileNumber.length-1);
			$(mobileCounter[0]).remove();
			mobileCart.append('<span class="menu-cart">'+mobileResult+'</span>');
		}
		
		if ($(mobileMenuCounter[0]).text() == "") {
			$(mobileMenuCounter[0]).remove();
		} else {
			
			var mobileMenuNumber = $(mobileMenuCounter[0]).text();
			var mobileMenuResult = mobileMenuNumber.substring(1, mobileMenuNumber.length-1);
			$(mobileMenuCounter[0]).remove();
			mobileMenuCart.append('<span class="menu-cart">'+mobileMenuResult+'</span>');
		}
	}

	///////////////////////////////////////
	// Language changes of Plugins START //
	///////////////////////////////////////
	var lang = $('html').attr('lang');
	if (lang == 'it-IT'){
		$('#vpc-add-to-cart').text('Aggiungi al carrello');
	}
	// MINICART
	$(document).on('click', '.menu-item.menu-item-type-post_type.menu-item-object-page', function() {
    setTimeout(function() {
        // This is where you can change the text in the minicart.
        // For example, to change the text of a specific element:
			if (lang == 'it-IT'){
				$('a.button.checkout.wc-forward.wp-element-button').text('Richiedi preventivo');
			} else {
				$('a.button.checkout.wc-forward.wp-element-button').text('Request a quote');
				$('.vpc-cart-component:contains("Colore per l\'interno:")').text('Internal color:');
				$('.vpc-cart-component:contains("Colore per l\'esterno:")').text('External 	color:');
			}
		}, 500); // Delay of 500 milliseconds. Adjust this as needed.
	});
	/////////////////////////////////////
	// Language changes of Plugins END //
	/////////////////////////////////////

});