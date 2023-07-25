<?php
/**
 * The public-facing functionality of the plugin.
 *
 * @link       http://www.orionorigin.com
 * @since      1.0.0
 *
 * @package    Vpc
 * @subpackage Vpc/public
 */

/**
 * The public-facing functionality of the plugin.
 *
 * Defines the plugin name, version, and two examples hooks for how to
 * enqueue the admin-specific stylesheet and JavaScript.
 *
 * @package    Vpc
 * @subpackage Vpc/public
 * @author     ORION <help@orionorigin.com>
 */
class VPC_Public {

	/**
	 * The ID of this plugin.
	 *
	 * @since    1.0.0
	 * @access   private
	 * @var      string    $plugin_name    The ID of this plugin.
	 */
	private $plugin_name;

	/**
	 * The version of this plugin.
	 *
	 * @since    1.0.0
	 * @access   private
	 * @var      string    $version    The current version of this plugin.
	 */
	private $version;

	/**
	 * Initialize the class and set its properties.
	 *
	 * @since    1.0.0
	 * @param      string $plugin_name       The name of the plugin.
	 * @param      string $version    The version of this plugin.
	 */
	public function __construct( $plugin_name, $version ) {

		$this->plugin_name = $plugin_name;
		$this->version     = $version;
	}

	/**
	 * Register the stylesheets for the public-facing side of the site.
	 *
	 * @since    1.0.0
	 */
	public function enqueue_styles() {
		wp_enqueue_style( 'vpc-public-css', VPC_URL . 'public/css/vpc-public.css', array(), VPC_VERSION, 'all' );
	}

	/**
	 * Register the stylesheets for the public-facing side of the site.
	 *
	 * @since    1.0.0
	 */
	public function enqueue_scripts() {
		wp_enqueue_script( 'vpc-accounting', VPC_URL . 'public/js/accounting.min.js', array( 'jquery' ), VPC_VERSION, false );
		wp_enqueue_script( 'vpc-public', VPC_URL . 'public/js/vpc-public.js', array( 'jquery', 'vpc-accounting', 'wp-hooks' ), VPC_VERSION, false );
		wp_localize_script('vpc-public', 'ajax_object', array('ajax_url' => admin_url('admin-ajax.php')));
	}

	/**
	 * Adds a new shortcode.
	 */
	public function register_shortcodes() {
		if ( ! is_admin() ) {
			add_shortcode( 'wpb_builder', array( $this, 'get_vpc_editor_handlers' ) );
			add_shortcode( 'vpc', array( $this, 'get_vpc_editor_handlers' ) );
		}
	}

	/**
	 * The callback function to run when the shortcode is found.
	 *
	 * @param array $atts The shortcode attributes.
	 */
	public function get_vpc_editor_handlers( $atts ) {
		$product_id = get_query_var( 'vpc-pid', false );

		// Maybe the product ID is included in the shortcode.
		if ( isset( $atts['product'] ) ) {
			$product = $atts['product'];
		}
		if ( ! $product_id ) {
			$product_id = $product;
		}

		if ( ! $product_id ) {
			$output = "<div class='VpcMsg'>" . __( "Looks like you're trying to access the configuration page directly. This page can only be accessed by clicking on the Build your own button from the product or the shop page.", 'vpc' ) . '</div>';
		} else {
			global $vpc_product_id;
			$vpc_product_id = $product_id;
			$output         = $this->get_vpc_editor( $product_id );
		}

		return $output;
	}

	/**
	 * The callback function to run when the shortcode is found.
	 *
	 * @param int $product_id The product id.
	 * @param int $config_id  The configuration id.
	 */
	public function get_vpc_editor( $product_id, $config_id = false ) {
		global $vpc_settings, $wp_query, $woocommerce;
		if ( class_exists( 'Woocommerce' ) ) {
			global $woocommerce;
			if ( $product_id ) {
				if ( vpc_woocommerce_version_check() ) {
					$product = new WC_Product( $product_id );
				} else {
					$product = wc_get_product( $product_id );
				}
				$config = get_product_config( $product_id );
			} elseif ( $config_id ) {
				$config = new VPC_Config( $config_id );
			}
		} else {
			$product_id = '';
			$config     = new VPC_Config( $config_id );
		}
		ob_start();
		?>
	<div class="all_images" style='display: none;'>
		<?php
		$settings = $config->settings;
		$nb_imgs  = 0;
		if ( isset( $settings['components'] ) ) {
			foreach ( $settings['components'] as $components ) {
				if ( isset( $components['options'] ) ) {
					foreach ( $components['options'] as $option ) {
						if ( class_exists( 'Vpc_Mva' ) && 'Yes' === $settings['multi-views'] ) {
							$views_arr = vpc_mva_get_config_views( $settings );
							foreach ( $views_arr as $key => $view ) {
								if ( isset( $option[ 'view_' . $key ] ) && ! empty( $option[ 'view_' . $key ] ) ) {
									$o_image = o_get_proper_image_url( $option[ 'view_' . $key ] );
									if ( is_numeric( $option['image'] ) ) {
											$opt_image_alt = get_post_meta( $option['image'], '_wp_attachment_image_alt', true );
									} else {
											$opt_image_alt = 'Visual Products Configurator option image';
									}
									echo "<img src='" . esc_attr( $o_image ) . "' alt='" . esc_attr( $opt_image_alt ) . "'>";
									$nb_imgs ++;
								}
							}
						} else {
							if ( ! empty( $option['image'] ) ) {
								$opt_image = o_get_proper_image_url( $option['image'] );
								if ( is_numeric( $option['image'] ) ) {
									$opt_image_alt = get_post_meta( $option['image'], '_wp_attachment_image_alt', true );
								} else {
									$opt_image_alt = 'Visual Products Configurator option image';
								}
								echo "<img src='" . esc_attr( $opt_image ) . "' alt='" . esc_attr( $opt_image_alt ) . "'>";
								$nb_imgs ++;
							}
						}
					}
				}
			}
		}
		?>
	</div>
		<?php
		$skin                   = get_proper_value( $config->settings, 'skin', 'VPC_Default_Skin' );
		$wvpc_conditional_rules = array();
		$reverse_triggers       = array();
		$rules_structure        = get_proper_value( $config->settings, 'conditional_rules', array() );
		$rules_enabled          = get_proper_value( $rules_structure, 'enable_rules', false );
		if ( 'enabled' === $rules_enabled ) {
			$rules_groups           = get_proper_value( $rules_structure, 'groups', array() );
			$reorganized_rules      = get_reorganized_rules( $rules_groups );
			$wvpc_conditional_rules = $reorganized_rules['per-option'];
			$reverse_triggers       = $reorganized_rules['reverse-triggers'];
		}
		$cart_url          = '';
		$product_url       = '';
		$price_format      = '';
		$decimal_separator = '';
		$symbol            = '';
		$price_separator   = '';
		$price_unit        = '';
		$to_load           = array();
		$cart_item_key     = '';
		if ( class_exists( 'Woocommerce' ) ) {
			if ( is_admin() && ! is_ajax() ) {
				$cart_url    = '';
				$product_url = '';
			} else {
				// Déclenche une erreur lorsqu'utilisée dans l'interface de conception d'un template.
				// $cart_url = $woocommerce->cart->get_cart_url();.
				if ( vpc_woocommerce_version_check() ) {
					$cart_url     = $woocommerce->cart->get_cart_url();
					$prod_id      = $product->id;
					$product_obj  = wc_get_product( $prod_id );
					$product_type = $product_obj->product_type;
					if ( 'variation' === $product_type ) {
						$prod_id = $product_obj->parent->id;
					}
				} else {
					$cart_url     = wc_get_cart_url();
					$prod_id      = $product->get_id();
					$product_obj  = wc_get_product( $prod_id );
					$product_type = $product_obj->get_type();
					if ( 'variation' === $product_type ) {
						$prod_id = $product_obj->get_parent_id();
					}
				}
				$product_url = get_permalink( $prod_id );
			}
		}

		if ( class_exists( 'Woocommerce' ) ) {
			$price_format      = vpc_get_price_format(); // phpcs:ignore // str_replace(html_entity_decode(htmlentities(get_woocommerce_currency_symbol())), "$", $raw_price_format);
			$decimal_separator = wc_get_price_decimal_separator();
			$symbol            = get_woocommerce_currency_symbol();
			$price_separator   = wc_get_price_thousand_separator();
			$price_unit        = wc_get_price_decimals();
		}

		$editor = new $skin( $product_id, $config_id );

		if ( isset( $wp_query->query_vars['edit'] ) ) {
			$cart_item_key = $wp_query->query_vars['edit'];
			$cart_content  = $woocommerce->cart->cart_contents;
			$item_content  = $cart_content[ $cart_item_key ];
			$to_load       = get_recap_from_cart_item( $item_content );
		}

		$to_load     = apply_filters( 'vpc_config_to_load', $to_load, $product_id );
		$canvas_data = array();
		if ( isset( $to_load['canvas_data'] ) ) {
			$canvas_data = json_decode( stripslashes( $to_load['canvas_data'] ) );
		}
		$canvas_data = apply_filters( 'vpc_canvas_data_to_load', $canvas_data, $to_load, $product_id );
		if ( isset( $wp_query->query_vars['edit'] ) ) {
			$cart_item_key = $wp_query->query_vars['edit'];
		}
		$ajax_loading             = get_proper_value( $vpc_settings, 'ajax-loading', 'No' );
		$action_after_add_to_cart = get_proper_value( $vpc_settings, 'action-after-add-to-cart', 'Yes' );

		$active_follow_scroll_desktop = get_proper_value( $vpc_settings, 'follow-scroll-desktop', 'Yes' );
		$active_follow_scroll_mobile  = get_proper_value( $vpc_settings, 'follow-scroll-mobile', 'No' );

		$config_image_sizes = get_config_images_size( $config->settings );
		$body_classes       = array( 'vpc-is-configurable', 'vpc-configurator' );
		if ( 'No' === $active_follow_scroll_desktop ) {
			array_push( $body_classes, 'vpc-desktop-follow-scroll-disabled' );
		}
		if ( 'No' === $active_follow_scroll_mobile ) {
			array_push( $body_classes, 'vpc-mobile-follow-scroll-disabled' );
		}

		$vpc_parameters = apply_filters(
			'vpc_data',
			array(
				'preload'                     => $to_load,
				'canvas_data'                 => $canvas_data,
				'product'                     => $product_id,
				'action_after_add_to_cart'    => $action_after_add_to_cart,
				'wvpc_conditional_rules'      => $wvpc_conditional_rules,
				'reverse_triggers'            => $reverse_triggers,
				'cart_url'                    => $cart_url,
				'current_product_page'        => $product_url,
				'vpc_selected_items_selector' => apply_filters( 'vpc_selected_items_selector', '.vpc-options input:checked, .vpc-options select > option:selected' ),
				'currency'                    => html_entity_decode( htmlentities( $symbol ) ),
				'decimal_separator'           => $decimal_separator,
				'thousand_separator'          => $price_separator,
				'decimals'                    => $price_unit,
				'price_format'                => $price_format,
				'config'                      => $config->settings,
				'trigger'                     => true,
				'enable_rules'                => get_proper_value( $rules_structure, 'enable_rules', false ),
				'select_first_elt'            => get_proper_value( $vpc_settings, 'select-first-elem', 'Yes' ),
				'query_vars'                  => array( 'edit' => $cart_item_key ),
				'ajax_loading'                => $ajax_loading,
				'nb_imgs'                     => $nb_imgs,
				'body_classes'                => $body_classes,
				'images_sizes'                => $config_image_sizes,
			)
		);
		?>

	<script>
		var vpc =<?php echo html_entity_decode( wp_json_encode( $vpc_parameters ) ); // phpcs:ignore ?>;
	</script>
		<?php
		// @codingStandardsIgnoreStart
		/*
		if ( $ajax_loading == 'Yes' && ! is_admin() ) {
		$editor->enqueue_styles_scripts();
		$output = "<div id='vpc-ajax-container' class=''><div id='vpc-ajax-loader-container' class='vpc-ajax-loader'><img src='" . VPC_URL . "public/images/preloader.gif'></div></div>";
		$output = apply_filters( 'vpc_ajax_lader_container', $output );
		} else { 
		 */
		// @codingStandardsIgnoreEnd
		if ( ! get_option( 'vpc-license-key' ) ) {
			$vpc_license_statut = vpc_activate_vpc_and_all_addons_licenses();
			// phpcs:ignore // $this->send_admin_email_about_license_status( 'vpc', $vpc_license_statut[ 'vpc' ][ 'vpc-checking' ] );
			$raw_output = vpc_get_error_message_license_is_not_active( $vpc_license_statut['vpc-status'] );
		} else {
			update_ajax_loading_option();
			vpc_enqueue_core_scripts();
			vpc_enqueue_core_styles();
			$image_content_output = ob_get_contents();
			$raw_output           = $image_content_output . $editor->display( $to_load );

		}
		$output = apply_filters( 'vpc_output_editor', $raw_output, $product_id, $config->id );
		// }
		ob_end_clean();
		return $output;
	}

	/**
	 * This function sends an email to the administrator on the status of the vpc license when there is a problem.
	 *
	 * @param String $product The product (vpc or slug of add-on name).
	 * @param String $reason The reason.
	 */
	private function send_admin_email_about_license_status( $product, $reason = '' ) {
		global $vpc_settings;
		$vpc_license = get_proper_value( $vpc_settings, 'purchase-code', '' );
		$headers     = array( 'Content-Type: text/html; charset=UTF-8' );
		$option      = ( get_option( $product . '-license-key' ) ) ? get_option( $product . '-license-key' ) : 'Empty';
		$message     = '';
		// phpcs:ignore // $transient = (get_transient($product . '-license-checking')) ? get_transient($product . '-license-checking') : "Empty";
		if ( 'Empty' !== $option ) {
			$to       = get_option( 'admin_email' );
			$subject  = 'Your product Visual Products Configurator license has been disabled on ' . site_url() . '.';
			$message .= nl2br( "You are receiving this email because your license for Visual Products Configurator has been deactivated. \n" );
			$message .= nl2br( "Please check your store and if you think that's an error, please contact our technical support at help@orionorigin.com. \n" );
		} else {
			$to       = 'vpc-monitoring@orionorigin.com';
			$subject  = 'License disabled but successfully re enabled automatically. ';
			$message .= nl2br( 'Site URL: ' . site_url() . ". \n" );
			$message .= nl2br( 'License key: ' . $vpc_license . ". \n" );
			$message .= nl2br( 'Reason: ' . $reason . ". \n" );
		}
		wp_mail( $to, $subject, $message, $headers );
	}

	/**
	 * Get vpc editor by ajax.
	 */
	public function get_vpc_editor_ajax() {
		$vpc        = $_POST['vpc']; // phpcs:ignore
		$to_load    = get_proper_value( $vpc, 'preload', false );
		$product_id = $_POST['vpc']['product']; // phpcs:ignore
		$config     = get_product_config( $product_id );
		$skin       = get_proper_value( $config->settings, 'skin', 'VPC_Default_Skin' );
		$editor     = new $skin( $product_id );
		if ( ! get_option( 'vpc-license-key' ) ) {
			$vpc_license_statut = vpc_activate_vpc_and_all_addons_licenses();
			// phpcs:ignore // $this->send_admin_email_about_license_status( 'vpc', $vpc_license_statut[ 'vpc' ][ 'vpc-checking' ] );
			$raw_output = vpc_get_error_message_license_is_not_active( $vpc_license_statut['vpc-status'] );
		} else {
			$raw_output = $editor->display( $to_load );
		}
		$output = apply_filters( 'vpc_output_editor', $raw_output, $product_id, $config->id );
		echo wp_kses( $output, get_allowed_tags() );
		die();
	}

	/**
	 * Function add query variables.
	 *
	 * @param array $a_vars Query variables datas.
	 */
	public function add_query_vars( $a_vars ) {
		// phpcs:ignore // $a_vars[] = "vpc-pid";
		$a_vars[] = 'edit';
		$a_vars[] = 'qty';
		return $a_vars;
	}

	/**
	 * Function rewrite configurator link.
	 *
	 * @param array $param Argument datas.
	 */
	public function add_rewrite_rules( $param ) {
		global $vpc_settings;
		global $wp_rewrite;
		add_rewrite_tag( '%vpc-pid%', '([^&]+)' );

		$config_page_id = get_proper_value( $vpc_settings, 'config-page', false );
		if ( ! $config_page_id ) {
			return;
		}

		$rule_str   = '';
		$rule_match = 1;
		$languages  = array();
		// @codingStandardsIgnoreStart
		/*
		if (function_exists('icl_get_languages')) {
		$languages_obj = apply_filters('wpml_active_languages', null, array('skip_missing' => false ));
		$languages = array_column($languages_obj, 'language_code');

		if(function_exists('pll_languages_list'))
		{
		$languages_str = implode("|", $languages);
		$rule_str = "($languages_str)/";
		$rule_match = 2;
		}
		} */
		// @codingStandardsIgnoreEnd
		if ( function_exists( 'icl_get_languages' ) ) {

			if ( function_exists( 'pll_languages_list' ) ) {
				$languages     = pll_languages_list();
				$languages_str = implode( '|', $languages );
				$rule_str      = "($languages_str)/";
				$rule_match    = 2;
			} else {
				if ( function_exists( 'icl_object_id' ) ) {
					$languages_obj = apply_filters( 'wpml_active_languages', null, array( 'skip_missing' => 1 ) );
					$languages     = array_column( $languages_obj, 'language_code' );
				}
			}
		}

		if ( is_array( $languages ) && ! empty( $languages ) ) {
			foreach ( $languages as $language_code ) {
				$translation_id  = icl_object_id( $config_page_id, 'page', true, $language_code );
				$translated_page = get_post( $translation_id );
				$slug            = $translated_page->post_name;
				if ( function_exists( 'pll_languages_list' ) ) {
					$wp_rewrite->add_rule( "$language_code/" . $slug . '/configure/([^/]+)', 'index.php?pagename=' . $slug . '&vpc-pid=$matches[1]', 'top' );
				} else {
					$wp_rewrite->add_rule( $slug . '/configure/([^/]+)', 'index.php?pagename=' . $slug . '&vpc-pid=$matches[1]', 'top' );
				}
			}
		} else {
			$wpc_page = get_post( $config_page_id );
			if ( is_object( $wpc_page ) ) {
				$slug = $wpc_page->post_name;
				if ( function_exists( 'pll_languages_list' ) ) {
					$wp_rewrite->add_rule( $rule_str . $slug . '/configure/([^/]+)', 'index.php?pagename=' . $slug . '&vpc-pid=$matches[' . $rule_match . ']', 'top' );
				} else {
					$wp_rewrite->add_rule( $slug . '/configure/([^/]+)', 'index.php?pagename=' . $slug . '&vpc-pid=$matches[' . $rule_match . ']', 'top' );
				}

				$wp_rewrite->flush_rules();
			}
		}
		if ( function_exists( 'pll_the_languages' ) ) {
			$rule_match = 1;

			$wpc_page = get_post( $config_page_id );
			if ( is_object( $wpc_page ) ) {
				$slug = $wpc_page->post_name;
				$wp_rewrite->add_rule( $slug . '/configure/([^/]+)', 'index.php?pagename=' . $slug . '&vpc-pid=$matches[' . $rule_match . ']', 'top' );

				$wp_rewrite->flush_rules();
			}
		}
	}

	/**
	 * Init globals variable for admin settings.
	 */
	public function init_globals() {
		global $vpc_settings;
		$vpc_settings = get_option( 'vpc-options' );
	}

	/**
	 * Display configure button.
	 */
	public function get_configure_btn() {
		$post_id = get_the_ID();
		$button  = $this->get_configuration_button( $post_id, true );
		if ( $button ) {
			echo wp_kses( $button, get_allowed_tags() );
		}
	}

	/**
	 * Hide add to cart button on shop page.
	 *
	 * @param string $product_id The product id.
	 */
	private function hide_add_to_cart_button_on_shop_page( $product_id ) {
		?>
	<script type="text/javascript">
		jQuery.each(jQuery('[data-product_id= "<?php echo esc_attr( $product_id ); ?>"]'), function () {
			if (jQuery(this).is('.button.product_type_simple.add_to_cart_button.ajax_add_to_cart')) {
				jQuery(this).hide();
				jQuery(this).attr('style', 'display:none !important');
			}
		});

	</script>
		<?php
	}

	/**
	 * Hide add to cart button on shop page.
	 *
	 * @param string $product_id The product id.
	 * @param string $product_type The product type.
	 */
	private function hide_add_to_cart_button( $product_id, $product_type ) {
		if ( 'variable' === $product_type ) {
			?>
		<script type="text/javascript">
			jQuery('form [value="<?php echo esc_attr( $product_id ); ?>"].single_add_to_cart_button').hide();
			jQuery('form [value="<?php echo esc_attr( $product_id ); ?>"].single_add_to_cart_button').attr('style', 'display:none !important');
		</script>
			<?php
		}
		?>
	<script type="text/javascript">
		setTimeout(function () {
		jQuery('form [data-product_id="<?php echo esc_attr( $product_id ); ?>"]').hide();
		jQuery('[value="<?php echo esc_attr( $product_id ); ?>"]').parent().find('.add_to_cart_button').hide();
		jQuery('[value="<?php echo esc_attr( $product_id ); ?>"]').parent().find('.single_add_to_cart_button').hide();
		jQuery('[value="<?php echo esc_attr( $product_id ); ?>"]').parent().find('.single_add_to_cart_button').attr('style', 'display:none !important');

		}, 500);
	</script>
		<?php
	}

	/**
	 * Get configuration button.
	 *
	 * @param string $product_id The product id.
	 * @param bool   $wrap       Display button or not.
	 */
	private function get_configuration_button( $product_id, $wrap = false ) {
		global $vpc_settings;
		$output = '';
		if ( class_exists( 'Woocommerce' ) ) {
			ob_start();
			$metas = get_post_meta( $product_id, 'vpc-config', true );

			$hide_wc_add_to_cart           = get_proper_value( $vpc_settings, 'hide-wc-add-to-cart', 'Yes' );
			$hide_add_to_cart_on_shop_page = get_proper_value( $vpc_settings, 'hide-wc-add-to-cart-on-shop-page', 'Yes' );
			$vpc_product_is_configurable   = vpc_product_is_configurable( $product_id );

			if ( $vpc_product_is_configurable && 'Yes' === $hide_add_to_cart_on_shop_page ) {
				$this->hide_add_to_cart_button_on_shop_page( $product_id );
			}

			$product = wc_get_product( $product_id );
			if ( vpc_woocommerce_version_check() ) {
				$product_type = $product->product_type;
			} else {
				$product_type = $product->get_type();
			}
			if ( 'variable' === $product_type ) {
				$variations = $product->get_available_variations();
				if ( isset( $variations ) && is_array( $variations ) ) {
					foreach ( $variations as $variation ) {
						$vpc_product_is_configurable = vpc_product_is_configurable( $variation['variation_id'] );
						echo wp_kses( $this->get_button( $variation['variation_id'], $metas, $wrap, false ), get_allowed_tags() );
						if ( $vpc_product_is_configurable ) {
							if ( 'Yes' === $hide_wc_add_to_cart ) {
								if ( vpc_woocommerce_version_check() ) {
									?>
					<script type="text/javascript">
						jQuery('form [data-product_id="<?php echo esc_attr( $variation['variation_id'] ); ?>"]').hide();
						jQuery('[value="<?php echo esc_attr( $variation['variation_id'] ); ?>"]').parent().find('.add_to_cart_button').hide();
						jQuery('[value="<?php echo esc_attr( $variation['variation_id'] ); ?>"]').parent().find('.single_add_to_cart_button').hide();
						jQuery('[value="<?php echo esc_attr( $variation['variation_id'] ); ?>"]').parent().find('.single_add_to_cart_button').attr('style', 'display:none !important');
					</script>
											<?php
								} else {
										$this->hide_add_to_cart_button( $product_id, $product_type );
								}
							}
							?>
				<script>
					jQuery(document).ready(function ($) {
					jQuery(document).on('change', 'input.variation_id', function () {
						$('.vpc-configure-button.button').each(function () {
						$(this).hide();
						});
						if ('' != $(this).val()) {
						$('.vpc-configure-button.button[data-id*="' + $(this).val() + '"]').show();
						}
					});
					});
				</script>
							<?php
						}
					}
				}
			} else {
				echo wp_kses( $this->get_button( $product_id, $metas, $wrap ), get_allowed_tags() );
				if ( $vpc_product_is_configurable && 'Yes' === $hide_wc_add_to_cart ) {
					$this->hide_add_to_cart_button( $product_id, $product_type );
				}
			}
			$output = ob_get_contents();
			ob_end_clean();
		}
		return $output;
	}
	/**
	 * Get button.
	 *
	 * @param string $id        Meta id.
	 * @param string $metas     Meta datas.
	 * @param bool   $wrap      Display button or not.
	 * @param bool   $display   Display button or not.
	 */
	private function get_button( $id, $metas, $wrap, $display = true ) {
		$configs    = get_proper_value( $metas, $id, array() );
		$config_id  = get_proper_value( $configs, 'config-id', false );
		$design_url = vpc_get_configuration_url( $id );
		if ( $display ) {
			$style = '';
		} else {
			$style = "style='display:none;'";
		}

		if ( ! $config_id ) {
			$design_url = apply_filters( 'vpc_build_your_own_button', false, $id, $style );
			return $design_url;
		} else {
			if ( $wrap ) {
				$design_url = "<a class='vpc-configure-button button' id='vpc-configure-button-$id' href='$design_url' data-id='$id' $style>" . __( 'Build your own', 'vpc' ) . '</a>';
			}
			?>
		<script>
			if (window.jQuery) {

			jQuery(document).ready(function ($) {
				var id = <?php echo esc_attr( $id ); ?>;
				jQuery(document).on('click', '#vpc-configure-button-' + id, function (e) {
				var link = $(this).attr('href');
				var qty = $(this).parents().find(".add_to_cart_button").data('quantity');
				if ( qty === 1 ) {
					link = link;
				} else {
					if (link.includes("?")) {
					link += '&qty=' + qty;
					} else {
					link += '?&qty=' + qty;
					}
				}
				$(this).attr('href', link);
				});
			});
			}
		</script>
			<?php
			$design_url = apply_filters( 'vpc_build_your_own_button', $design_url, $id, $style );
			return $design_url;
		}
	}

	/**
	 * Get configuration button.
	 *
	 * @param string $html        Button container.
	 * @param object $product     Product object.
	 */
	public function get_configure_btn_loop( $html, $product ) {
		global $vpc_settings;
		$hide_build_your_own_btn = get_proper_value( $vpc_settings, 'hide-build-your-own', 'No' );
		if ( 'No' === $hide_build_your_own_btn ) {
			$button = $this->get_configuration_button( $product->get_id(), true );
			if ( $button ) {
				$html .= $button;
			}
		}
		else{
			ob_start();
			$vpc_product_is_configurable = vpc_product_is_configurable( $product->get_id() );
			$hide_add_to_cart_on_shop_page = get_proper_value( $vpc_settings, 'hide-wc-add-to-cart-on-shop-page', 'Yes' );
			if ( $vpc_product_is_configurable && 'Yes' === $hide_add_to_cart_on_shop_page ) {
				$this->hide_add_to_cart_button_on_shop_page( $product->get_id() );
			}
			$output = ob_get_contents();
			ob_end_clean();
			$html .= $output;
		}
		return $html;
	}

	/**
	 * Add filter to display editor on manage page.
	 */
	public function set_variable_action_filters() {
		global $vpc_settings;
		$append_content_filter = get_proper_value( $vpc_settings, 'manage-config-page', 'Yes' );

		if ( 'Yes' === $append_content_filter && ! is_admin() ) {
			add_filter( 'the_content', array( $this, 'filter_content' ), 99 );
		}
	}

	/**
	 * Function to display editor content on manage page.
	 *
	 * @param string $content The page content.
	 */
	public function filter_content( $content ) {
		global $vpc_settings;
		$vpc_page_id    = get_proper_value( $vpc_settings, 'config-page', false );
		$vpc_page_id    = apply_filters( 'vpc_configurator_page_id', $vpc_page_id );
		$product_object = (object) array();
		if ( ! $vpc_page_id ) {
			return $content;
		}
		if ( function_exists( 'icl_object_id' ) ) {
			$vpc_page_id = icl_object_id( $vpc_page_id, 'page', true, ICL_LANGUAGE_CODE );
		}

		$current_page_id = get_the_ID();
		if ( intval( $vpc_page_id ) === $current_page_id ) {

			$product_id = get_query_var( 'vpc-pid', false );
			$product_id = apply_filters( 'vpc_configurator_product_id', $product_id );
			if ( class_exists( 'Woocommerce' ) ) {
				$product_object = wc_get_product( $product_id );
			} else {
				$product_id     = '';
				$product_object = (object) array();
			}
			if ( ! $product_id ) {
				$content .= "<div class='VpcMsg'>" . __( "Looks like you're trying to access the configuration page directly. This page can only be accessed by clicking on Build your own button from the product or the shop page.", 'vpc' ) . '</div>';
			} elseif ( ( $product_object && ! $product_object->is_purchasable() ) || ( $product_object && ! $product_object->is_in_stock() ) ) {
				$content .= __( 'This product is not purchasable.', 'vpc' );
			} else {
				$content .= $this->get_vpc_editor( $product_id );
			}
		}
		return $content;
	}

	// @codingStandardsIgnoreStart
	// public function get_design_price() {
	// $price = $_POST["total_price"];
	// echo wc_price($price);
	// die();
	// }
	// @codingStandardsIgnoreEnd

	/**
	 * Function to display editor content on manage page.
	 *
	 * @param string $id          Unique id.
	 * @param string $image_data  Image data.
	 */
	public function vpc_get_image_url( $id, $image_data ) {
		$upload_dir      = wp_upload_dir();
		$generation_path = $upload_dir['basedir'] . '/VPC';
		$generation_url  = $upload_dir['baseurl'] . '/VPC';
		$final_file_url  = '';
		if ( wp_mkdir_p( $generation_path ) ) {
			$final_file_path = $generation_path . '/canvas_' . $id . '.png';
			$final_file_url  = $generation_url . '/canvas_' . $id . '.png';
			$unencoded       = base64_decode( $image_data ); // phpcs:ignore
			$fp              = fopen( $final_file_path, 'w' ); // phpcs:ignore
			fwrite( $fp, $unencoded ); // phpcs:ignore
			fclose( $fp ); // phpcs:ignore
		}
		return $final_file_url;
	}

	/**
	 * Ajax callback to configuration to cart.
	 */
	public function add_vpc_configuration_to_cart() {
		global $woocommerce;
		$message = '';
		if ( vpc_woocommerce_version_check() ) {
			$cart_url = $woocommerce->cart->get_cart_url();
		} else {
			$cart_url = wc_get_cart_url();
		}
		$cart_content = $woocommerce->cart->cart_contents;
		$product_id   = $_POST['product_id']; // phpcs:ignore
		if ( isset( $_POST['quantity'] ) ) { // phpcs:ignore
			$quantity = $_POST['quantity']; // phpcs:ignore
		} else {
			$quantity = 1;
		}

		// phpcs:ignore // $recap = $_POST['recap']; 
		$recap = (array) json_decode( stripslashes( $_POST['recap'] ) ); // phpcs:ignore
		// Remove empty compenents.
		if ( isset( $recap ) && ! empty( $recap ) ) {
			foreach ( $recap as $key => $value ) {
				if ( '' === $value ) {
					unset( $recap[ $key ] );
				}
			}
		}

		$custom_vars = '';
		if ( $_POST['custom_vars'] ) { // phpcs:ignore
			$custom_vars = $_POST['custom_vars']; // phpcs:ignore
		}
		$preview_urls = vpc_get_merged_image( $custom_vars );
		if ( is_array( $preview_urls ) ) {
			$custom_vars['preview_saved'] = $preview_urls[0];
			unset( $custom_vars['preview_imgs_merged'] );
		}

		if ( class_exists( 'Ofb' ) ) {
			if ( isset( $_POST['form_data'] ) ) { // phpcs:ignore
				$form_data = $_POST['form_data']; // phpcs:ignore
			}
		}

		$alt_products = array();
		if ( isset( $_POST['alt_products'] ) ) { // phpcs:ignore
			$alt_products = $_POST['alt_products']; // phpcs:ignore
		}
		if ( ! is_array( $alt_products ) ) {
			$alt_products = array();
		}

		$proceed_addition_to_cart = apply_filters( 'vpc_proceed_add_to_cart', true, $_POST ); // phpcs:ignore
		// Check if there is enought items in the stock.
		$products_are_availables = $this->check_product_availability( $product_id, $quantity );
		if ( $proceed_addition_to_cart && ! empty( $alt_products ) ) {
			foreach ( $alt_products as $key => $alt_product_id ) {
				if ( ! $this->check_product_availability( $alt_product_id, $quantity ) ) {
					$products_are_availables = false;
				}
			}
		}
		if ( ! $products_are_availables ) {
			$message = __( 'You can not add that amount of product to the cart', 'vpc' );
			echo esc_html( $message );
			die();
		}

		$ids          = get_product_root_and_variations_ids( $product_id );
		$variation_id = $ids['variation-id'];
		if ( $proceed_addition_to_cart && $products_are_availables ) {
			if ( isset( $_COOKIE['attributes'][ $variation_id ] ) && ! empty( $_COOKIE['attributes'][ $variation_id ] ) ) {
				$custom_vars['attributes'] = $_COOKIE['attributes'][ $variation_id ]; // phpcs:ignore
				unset( $_COOKIE['attributes'][ $variation_id ] );
			}
			if ( isset( $custom_vars['item_key'] ) && ! empty( $custom_vars['item_key'] ) ) {
				$newly_added_cart_item_key = $custom_vars['item_key'];

				// Remove old alternate products from the cart.
				if ( isset( $woocommerce->cart->cart_contents ) && ! empty( $woocommerce->cart->cart_contents ) ) {
					foreach ( $woocommerce->cart->cart_contents as $to_del_cart_key => $to_del_cart_value ) {
						if ( array_key_exists( 'vpc-is-secondary-product', $to_del_cart_value ) ) {
							if ( $newly_added_cart_item_key === $to_del_cart_value['main_product_cart_item_key'] ) {
								unset( WC()->cart->cart_contents[ $to_del_cart_key ] );
							}
						}
					}
				}

				$old_custom_vars = $cart_content[ $newly_added_cart_item_key ]['vpc-custom-vars'];
				$new_data        = $recap;
				$new_custom_data = array_replace( $old_custom_vars, $custom_vars );

				$woocommerce->cart->cart_contents[ $newly_added_cart_item_key ]['visual-product-configuration'] = $new_data;
				$woocommerce->cart->cart_contents[ $newly_added_cart_item_key ]['vpc-custom-vars']              = $new_custom_data;
				$woocommerce->cart->set_quantity( $newly_added_cart_item_key, $quantity );
				if ( class_exists( 'Ofb' ) ) {
					if ( isset( $form_data ) ) {
						$old_form_data = $cart_content[ $newly_added_cart_item_key ]['form_data'];
						$new_form_data = array_replace( $old_form_data, $form_data );
						// phpcs:ignore // $new_form_data = $form_data;
						$woocommerce->cart->cart_contents[ $newly_added_cart_item_key ]['form_data'] = $new_form_data;
					}
				}
				$woocommerce->cart->calculate_totals();
			} else {
				if ( vpc_woocommerce_version_check() ) {
					if ( isset( $form_data ) ) {
						$newly_added_cart_item_key = $woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							$ids['variation'],
							array(
								'visual-product-configuration' => $recap,
								'vpc-custom-vars' => $custom_vars,
								'form_data'       => $form_data,
							)
						);
					} else {
						$newly_added_cart_item_key = $woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							$ids['variation'],
							array(
								'visual-product-configuration' => $recap,
								'vpc-custom-vars' => $custom_vars,
							)
						);
					}
				} else {
					if ( isset( $form_data ) ) {
						$newly_added_cart_item_key = $woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							'',
							array(
								'visual-product-configuration' => $recap,
								'vpc-custom-vars' => $custom_vars,
								'form_data'       => $form_data,
							)
						);
					} else {
						$newly_added_cart_item_key = $woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							'',
							array(
								'visual-product-configuration' => $recap,
								'vpc-custom-vars' => $custom_vars,
							)
						);
					}
				}
			}

			// phpcs:ignore // print_r($woocommerce->cart->cart_contents);
			do_action( 'vpc_add_to_cart_main', $ids['product-id'], $quantity, $ids['variation-id'] );
			if ( method_exists( $woocommerce->cart, 'maybe_set_cart_cookies' ) ) {
				$woocommerce->cart->maybe_set_cart_cookies();
			}
			if ( $newly_added_cart_item_key ) {
				// Alternate products.
				foreach ( $alt_products as $alt_product_id ) {
					$ids = get_product_root_and_variations_ids( $alt_product_id );
					if ( vpc_woocommerce_version_check() ) {
						$woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							$ids['variation'],
							array(
								'vpc-is-secondary-product' => true,
								'main_product_cart_item_key' => $newly_added_cart_item_key,
							)
						);
						if ( method_exists( $woocommerce->cart, 'maybe_set_cart_cookies' ) ) {
									$woocommerce->cart->maybe_set_cart_cookies();
						}
					} else {
						$woocommerce->cart->add_to_cart(
							$ids['product-id'],
							$quantity,
							$ids['variation-id'],
							'',
							array(
								'vpc-is-secondary-product' => true,
								'main_product_cart_item_key' => $newly_added_cart_item_key,
							)
						);
						if ( method_exists( $woocommerce->cart, 'maybe_set_cart_cookies' ) ) {
							$woocommerce->cart->maybe_set_cart_cookies();
						}
					}
					do_action( 'vpc_add_to_cart_alt', $ids['product-id'], $quantity, $ids['variation-id'] );
				}
				$raw_message = "<div class='vpc-success f-right'>" . __( 'Product successfully added to basket.', 'vpc' ) . " <a href='$cart_url'>" . __( 'View Cart', 'vpc' ) . '</a></div>';
				$message     = apply_filters( 'vpc_add_to_cart_success_message', $raw_message );
			} else {
				$raw_message = "<div class='vpc-failure f-right'>" . __( 'A problem occured. Please try again.', 'vpc' ) . '</div>';
				$message     = apply_filters( 'vpc_add_to_cart_failure_message', $raw_message );
			}
			echo wp_kses( $message, get_allowed_tags() );
		} else {
			do_action( 'vpc_add_to_cart_processing', $_POST ); // phpcs:ignore
		}
		die();
	}

	/**
	 * Function to get configurator image outpout.
	 *
	 * @param string $product_image_code  The product image output.
	 * @param array  $values              Item values.
	 * @param string $cart_item_key       Cart item cart key.
	 */
	public function get_vpc_data_image( $product_image_code, $values, $cart_item_key ) {
		if ( $values['variation_id'] ) {
			$product_id = $values['variation_id'];
		} else {
			$product_id = $values['product_id'];
		}
		$config = get_product_config( $product_id );
		// We extract the recap from the cart item key.
		$recap = get_recap_from_cart_item( $values );
		if ( ! empty( $recap ) ) {
			$config_image       = $this->get_config_image( $recap, $config->settings, $values );
			$product_image_code = $config_image;
		}
		return $product_image_code;
	}

	/**
	 * Function to get configurator data in cart.
	 *
	 * @param string $thumbnail_code      The configurator datas output in cart.
	 * @param array  $values              Item values.
	 * @param string $cart_item_key       Cart item cart key.
	 */
	public function get_vpc_data( $thumbnail_code, $values, $cart_item_key ) {
		global $woocommerce, $vpc_settings;
		if ( $values['variation_id'] ) {
			$product_id = $values['variation_id'];
		} else {
			$product_id = $values['product_id'];
		}
		$config = get_product_config( $product_id );
		// We extract the recap from the cart item key.
		$recap = get_recap_from_cart_item( $values );

		$thumbnail_code = apply_filters( 'vpc_get_cart_item_name', $thumbnail_code, $product_id, $recap, $config );

		if ( ! empty( $recap ) ) {
			if ( isset( $values['vpc-custom-vars']['attributes'] ) && ! empty( $values['vpc-custom-vars']['attributes'] ) ) {
				$details = '';
				foreach ( $values['vpc-custom-vars']['attributes'] as $key => $value ) {
					$name     = explode( '_', $key );
					$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
        <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
				}
				$thumbnail_code .= '<dl class="variation">' . $details . '</dl>';
			}
			if ( 'No' === get_proper_value( $vpc_settings, 'hide-options-selected-in-cart', 'No' ) ) {
				$formatted_config = $this->get_formatted_config_data( $recap, $config->settings, $values );
				$thumbnail_code  .= "<div class='vpc-cart-config o-wrap'><div class='o-col xl-1-1'>" . $formatted_config . '</div> </div>';
			}
		}

		$config_url   = vpc_get_configuration_url( $product_id );
		$cart_content = $woocommerce->cart->cart_contents;
		$item_content = $cart_content[ $cart_item_key ];

		$vpc_config_metas = get_post_meta( $product_id, 'vpc-config', true );

		if ( isset( $vpc_config_metas[ $product_id ]['config-edit-link'] ) && '' !== $vpc_config_metas[ $product_id ]['config-edit-link'] ) {

			$config_page_id = get_proper_value( $vpc_settings, 'config-page', false );
			if ( 0 !== intval( $vpc_config_metas[ $product_id ]['config-edit-link'] ) && 1 !== intval( $vpc_config_metas[ $product_id ]['config-edit-link'] ) && intval( $vpc_config_metas[ $product_id ]['config-edit-link'] ) !== intval( $config_page_id ) ) {
				$edit_url = get_permalink( $vpc_config_metas[ $product_id ]['config-edit-link'] ) . "?edit=$cart_item_key&qty=" . $item_content['quantity'];
			} else {
				$edit_url = $config_url . "?edit=$cart_item_key&qty=" . $item_content['quantity'];
			}
		} elseif ( get_option( 'permalink_structure' ) ) {
			$edit_url = $config_url . "?edit=$cart_item_key&qty=" . $item_content['quantity'];
		} else {
			$edit_url = $config_url . "&edit=$cart_item_key&qty=" . $item_content['quantity'];
		}
		// if ( isset( $item_content['visual-product-configuration'] ) ) {
		// 	$thumbnail_code .= '<a class="button alt vpc-edit-config-button" href="' . $edit_url . '">' . __( 'Edit', 'vpc' ) . '</a>';
		// }

		$thumbnail_code = apply_filters( 'vpc_get_config_data', $thumbnail_code, $recap, $config, $values, $cart_item_key );
		return $thumbnail_code;
	}

	/**
	 * Function to get configurator image outpoup in cart.
	 *
	 * @param array $recap      The configurator recap datas.
	 * @param array $config     Configuration datas.
	 * @param array $item       Cart item.
	 */
	public static function get_config_image( $recap, $config, $item ) {
		$output = '';
		if ( is_array( $recap ) ) {
			if ( isset( $item['vpc-custom-vars']['preview_saved'] ) && ! empty( $item['vpc-custom-vars']['preview_saved'] ) ) {
				if ( ! is_array( $item['vpc-custom-vars']['preview_saved'] ) ) {
					$url    = $item['vpc-custom-vars']['preview_saved'];
					$output = "<img src='" . $url . "' alt='Visual Product Configurator preview image' />";
				}
			} elseif ( isset( $item['vpc-custom-data']['preview_saved'] ) && ! empty( $item['vpc-custom-data']['preview_saved'] ) ) {
				if ( ! is_array( $item['vpc-custom-data']['preview_saved'] ) ) {
					$url    = $item['vpc-custom-data']['preview_saved'];
					$output = "<img src='" . $url . "' alt='Visual Product Configurator preview image'/>";
				}
			} else {
				$output = "<img src='" . $this->get_config_image_by_image_merged( $recap, $config, $item ) . "' alt='Visual Product Configurator preview image'/>";
			}
			$output = "<div class='vpc-cart-config-image o-wrap'>$output</div>";
		}
		$output = apply_filters( 'vpc_get_config_image', $output, $recap, $config, $item );
		return $output;
	}

	/**
	 * Function to get configurator image by image merged.
	 *
	 * @param array $recap      The configurator recap datas.
	 * @param array $config     Configuration datas.
	 * @param array $item       Cart item.
	 */
	private function get_config_image_by_image_merged( $recap, $config, $item ) {
		$output = '';
		$imgs   = array();
		if ( is_array( $recap ) ) {
			foreach ( $recap as $component => $raw_options ) {
				if ( is_array( $raw_options ) ) {
					// phpcs:ignore // $options=  implode (", ", $raw_options);
					foreach ( $raw_options as $options ) {
						$image   = self::extract_option_field_from_config( $options, $component, $config, 'image' );
						$img_src = o_get_proper_image_url( $image );
						$title   = $raw_options;
						if ( is_array( $raw_options ) ) {
							$title = implode( ', ', $raw_options );
						}
						if ( isset( $img_src ) && ! empty( $img_src ) ) {
							// phpcs:ignore // $img_code = "<img src='$img_src' data-tooltip-title='$title'>";
							// phpcs:ignore // $output.=$img_code;
							array_push( $imgs, $img_src );
						}
					}
				} else {
					$options = $raw_options;
					$image   = self::extract_option_field_from_config( $raw_options, $component, $config, 'image' );
					$img_src = o_get_proper_image_url( $image );
					$title   = $raw_options;
					if ( is_array( $raw_options ) ) {
						$title = implode( ', ', $raw_options );
					}
					if ( isset( $img_src ) && ! empty( $img_src ) ) {
						// phpcs:ignore // $img_code = "<img src='$img_src' data-tooltip-title='$title'>";
						// phpcs:ignore // $output.=$img_code;
						array_push( $imgs, $img_src );
					}
				}
			}
			$img_url = merge_pictures( $imgs, false, true );
		}

		return $img_url;
	}

	/**
	 * Function to get configurator image by image merged.
	 *
	 * @param array $recap        The configurator recap datas.
	 * @param array $config       Configuration datas.
	 * @param bool  $show_icons   Show option icon or not.
	 */
	public function get_formatted_config_data( $recap, $config, $show_icons = true ) {
		$output         = "<div class='vpc-cart-options-container'>";
		$option         = '';
		$filtered_recap = apply_filters( 'vpc_filter_recap', $recap, $config, $show_icons );

		if ( is_array( $filtered_recap ) ) {
			foreach ( $filtered_recap as $component => $raw_options ) {
				$options_arr = $raw_options;
				if ( ! is_array( $raw_options ) ) {
					$options_arr = array( $raw_options );
				}
				$options_html = '';
				$labels_html  = '';
				if ( $show_icons ) {
					foreach ( $options_arr as $option ) {
						$icon     = self::extract_option_field_from_config( $option, $component, $config );
						$img_code = '';
						if ( $icon ) {
							$img_src = o_get_proper_image_url( $icon );
							if ( is_numeric( $icon ) ) {
								$img_alt = get_post_meta( $icon, '_wp_attachment_image_alt', true );
							} else {
								$img_alt = 'Visual Products Configurator option icon image';
							}
							$img_code = "<div class='vpc-cart-options'><div><div>" . stripslashes( $option ) . "</div><div><img src='$img_src' alt='$img_alt' data-tooltip-title='$option'></div></div></div>";
							// phpcs:ignore // $img_code = "<img src='$img_src' data-tooltip-title='$option'>";
							$options_html .= $img_code;
						} else {
							$options_html .= "<div class='vpc-cart-options addon-options'>" . stripslashes( $option ) . '</div>'; // To escape quotes in the name.
						}
					}
				} else {
					$options_html = "<div class='vpc-cart-options'>" . implode( ', ', $options_arr ) . '</div>';
				}
				$option = stripslashes( $option );

				foreach ( $config['components'] as $comp_key => $components ) {
					if ( $component !== $components['cname'] ) {
						if ( isset( $components['options'] ) ) {
							foreach ( $components['options'] as $option_key => $option_value ) {
								$name_value = $components['cname'] . ' ' . $option_value['group'];
								if ( $component === $name_value ) {
									$component = $components['cname'];
								}
							}
						}
					}
				}

				$component = stripslashes( $component );

				$output .= "<div><div class='vpc-cart-component'>$component: </div>$options_html</div>";
			}
		}
		$output .= '</div>';
		return apply_filters( 'get_formatted_config_data', $output, $recap, $config, $show_icons );
	}

	/**
	 * Function to extract option field from configurator.
	 *
	 * @param string $searched_option        Option name.
	 * @param string $searched_component     Component name.
	 * @param array  $config                 Configuration datas.
	 * @param string $field                  Option field name.
	 */
	public static function extract_option_field_from_config( $searched_option, $searched_component, $config, $field = 'icon' ) {
		$unslashed_searched_option = vpc_remove_special_characters( $searched_option );
		$field                     = apply_filters( 'extracted_option_field_from_config', $field, $config );
		if ( ! is_array( $config ) ) {
			$config = unserialize( $config ); // phpcs:ignores
		}
		if ( isset( $config['components'] ) ) {
			foreach ( $config['components'] as $i => $component ) {
				if ( isset( $component['options'] ) ) {
					foreach ( $component['options'] as $component_option ) {
						$name_value = $component['cname'] . ' ' . $component_option['group'];
						if ( $searched_component === $name_value ) {
							$searched_component = $component['cname'];
						}
						$unslashed_searched_component = vpc_remove_special_characters( $searched_component );
						if ( vpc_remove_special_characters( $component['cname'], '"' ) === $unslashed_searched_component ) {
							if ( vpc_remove_special_characters( $component_option['name'], '"' ) === $unslashed_searched_option ) {
								if ( isset( $component_option[ $field ] ) ) {
									return $component_option[ $field ];
								}
							}
						}
					}
				}
			}
		}
		return false;
	}
	// @codingStandardsIgnoreStart
	/*
	 function save_customized_item_meta( $item_id, $values, $cart_item_key ) {
	  global $vpc_settings;
	  $store_original_config = get_proper_value( $vpc_settings, 'store-original-configs', 'Yes' );

	  if ( $values[ 'variation_id' ] ) {
	  $product_id = $values[ 'variation_id' ];
	  } else {
	  $product_id = $values[ 'product_id' ];
	  }

	  // We extract the recap from the cart item key
	  $recap		 = get_recap_from_cart_item( $values );
	  $original_config = get_product_config( $product_id );
	  /*
	  if (isset($values['vpc-is-secondary-product']))
	  wc_add_order_item_meta($item_id, 'vpc-is-secondary-product', $values['vpc-is-secondary-product']); */
	/*
	 if ( ! empty( $recap ) && $original_config != false ) {
	  wc_add_order_item_meta( $item_id, 'vpc-cart-data', $recap );
	  if ( ! empty( $values[ 'vpc-custom-vars' ] ) ) {
	  wc_add_order_item_meta( $item_id, 'vpc-custom-data', $values[ 'vpc-custom-vars' ] );
	  }
	  if ( $store_original_config == 'Yes' ) {
	  wc_add_order_item_meta( $item_id, 'vpc-original-config', $original_config->settings );
	  }
	  }
	  // if(class_exists('Ofb')){
	  // $form_data = get_form_data_from_cart_item($values);
	  // if(!empty($form_data) && $original_config != false)
	  // wc_add_order_item_meta($item_id, 'form_data', $form_data);
	  // }
	  }
	 */
	// @codingStandardsIgnoreEnd

	/**
	 * Add vpc data to item before save.
	 *
	 * @param object $item          Item object.
	 * @param string $cart_item_key The cart item key.
	 * @param array  $values        Item datas.
	 * @param object $order         The Order instance.
	 */
	public function add_customized_item_meta( $item, $cart_item_key, $values, $order ) {
		global $vpc_settings;
		$store_original_config = get_proper_value( $vpc_settings, 'store-original-configs', 'Yes' );

		if ( $values['variation_id'] ) {
			$product_id = $values['variation_id'];
		} else {
			$product_id = $values['product_id'];
		}

		$recap           = get_recap_from_cart_item( $values );
		$original_config = get_product_config( $product_id );

		if ( $recap && ! empty( $recap ) ) {
			$item->update_meta_data( 'vpc-cart-data', $recap );
			if ( $values['vpc-custom-vars'] && ! empty( $values['vpc-custom-vars'] ) ) {
				$item->update_meta_data( 'vpc-custom-data', $values['vpc-custom-vars'] );
			}
			if ( 'Yes' === $store_original_config ) {
				$item->update_meta_data( 'vpc-original-config', $original_config->settings );
			}
		}
		if ( true === $values['vpc-is-secondary-product'] ) {
			$item->update_meta_data( 'vpc-is-secondary-product', $values['vpc-is-secondary-product'] );
		}
	}

	/**
	 * Get user account products meta.
	 *
	 * @param string $output Configurator datas output in order.
	 * @param object $item   Item object.
	 */
	public function get_user_account_products_meta( $output, $item ) {
		if ( isset( $item['vpc-cart-data'] ) ) {
			$original_config = vpc_get_order_item_configuration( $item );
			$output         .= '<br>';

			if ( vpc_woocommerce_version_check() ) {
				$recap = unserialize( $item['vpc-cart-data'] ); // phpcs:ignore
			} else {
				$recap = $item['vpc-cart-data'];
			}
			if ( ! empty( $recap ) ) {
				if ( isset( $item['vpc-custom-data']['attributes'] ) && ! empty( $item['vpc-custom-data']['attributes'] ) ) {
					$details = '';
					foreach ( $item['vpc-custom-data']['attributes'] as $key => $value ) {

						$name     = explode( '_', $key );
						$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
          <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
					}
					$output .= '<dl class="variation">' . $details . '</dl>';
				}
			}

			$config_image     = $this->get_config_image( $recap, $original_config, $item );
			$formatted_config = $this->get_formatted_config_data( $recap, $original_config );
			$output          .= "<div class='vpc-cart-config o-wrap'>" . $config_image . "<div class='o-col xl-2-3'>" . $formatted_config . '</div></div>';
		}
		// @codingStandardsIgnoreStart
		// if(class_exists('Ofb')){
		// if (isset($item["form_data"])) {
		// var_dump($item["form_data"]);
		// $form_data = $item["form_data"];
		// $form_html =  $this->get_form_build_data($form_data);
		// $output.= "<div><div class='o-col xl-2-3'>" . $form_html . "</div> </div>";
		// }
		// }
		// @codingStandardsIgnoreEnd
		return $output;
	}

	/**
	 * Get admin products metas.
	 *
	 * @param string $item_id    Item id.
	 * @param object $item       Item object.
	 * @param object $_product   Product object.
	 */
	public function get_admin_products_metas( $item_id, $item, $_product ) {
		$output = '';
		if ( isset( $item['vpc-cart-data'] ) ) {
			$original_config = vpc_get_order_item_configuration( $item );
			$output         .= '<br>';
			if ( vpc_woocommerce_version_check() ) {
				$recap = unserialize( wp_strip_all_tags( $item['vpc-cart-data'] ) ); // phpcs:ignore
			} else {
				$recap = $item['vpc-cart-data'];
			}
			if ( ! empty( $recap ) ) {
				if ( isset( $item['vpc-custom-data']['attributes'] ) && ! empty( $item['vpc-custom-data']['attributes'] ) ) {
					$details = '';
					foreach ( $item['vpc-custom-data']['attributes'] as $key => $value ) {

						$name     = explode( '_', $key );
						$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
          <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
					}
					$output .= '<dl class="variation">' . $details . '</dl>';
				}
			}
			$config_image     = $this->get_config_image( $recap, $original_config, $item );
			$formatted_config = $this->get_formatted_config_data( $recap, $original_config );
			$output          .= "<div class='vpc-order-config o-wrap xl-gutter-8'>" . $config_image . "<div class='o-col xl-2-3'>" . $formatted_config . '</div></div>';
		}
		echo wp_kses( $output, get_allowed_tags() );
	}

	/**
	 * Get product linked price.
	 *
	 * @param string $linked_product    Linked product id.
	 */
	public static function get_product_linked_price( $linked_product ) {
		global $vpc_settings;
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );
		if ( 'Yes' === $hide_secondary_product_in_cart ) {
			$_product = wc_get_product( $linked_product );
			if ( function_exists( 'wad_get_product_price' ) ) {
				$option_price = wad_get_product_price( $_product );
			} else {
				//phpcs:ignore // $option_price = $_product->get_price();
				$option_price = $_product->get_regular_price();
				if ( strpos( $option_price, ',' ) ) {
					$option_price = floatval( str_replace( ',', '.', $option_price ) );
				}
			}
		} else {
			$option_price = 0;
		}
		return $option_price;
	}

	/**
	 * Get configurator price.
	 *
	 * @param string $product_id            Linked product id.
	 * @param array  $config                Configuration datas.
	 * @param object $cart_item             Item object.
	 * @param bool   $statut                Statut.
	 * @param bool   $apply_wad_discount    Apply wad discount or not.
	 */
	public static function get_config_price( $product_id, $config, $cart_item, $statut = false, $apply_wad_discount = true ) {
		if ( ! get_option( 'vpc-license-key' ) ) {
			return;
		}
		$original_config = get_product_config( $product_id );
		$total_price     = 0;
		$product         = wc_get_product( $product_id );
		if ( is_array( $config ) ) {
			foreach ( $config as $component => $raw_options ) {
				$options_arr = $raw_options;
				if ( ! is_array( $raw_options ) ) {
					$options_arr = array( $raw_options );
				}
				foreach ( $options_arr as $option ) {
					$linked_product = self::extract_option_field_from_config( $option, $component, $original_config->settings, 'product' );
					$option_price   = self::extract_option_field_from_config( $option, $component, $original_config->settings, 'price' );

					if ( strpos( $option_price, ',' ) ) {
						$option_price = floatval( str_replace( ',', '.', $option_price ) );
					}
					if ( $linked_product ) {
						$option_price = self::get_product_linked_price( $linked_product );
						$option_price = vpc_get_opt_price_before_dicount_in_cart( $product_id, $linked_product, $option_price, $statut );
					}

					// We make sure we're not handling any empty priced option.
					if ( empty( $option_price ) ) {
						if ( ! $linked_product ) {
							$option_price = self::extract_option_field_from_config( $option, $component, $original_config->settings, 'price' );
							if ( false !== $option_price && $apply_wad_discount ) {
								$option_price = 0;
								$option_price = vpc_get_wad_discount_for_opt_in_cart( $product_id, $option_price );
							} else {
								$option_price = 0;
							}
						} else {
							$option_price = 0;
						}
					} else {
						if ( ! $linked_product && $apply_wad_discount ) {
							$option_price = vpc_get_wad_discount_for_opt_in_cart( $product_id, $option_price );
						}
					}
					$total_price += $option_price;
				}
			}
		}
		return apply_filters( 'vpc_config_price', $total_price, $product_id, $config, $cart_item, $statut );
	}

	/**
	 * Get cart item price.
	 *
	 * @param object $cart     Cart object.
	 */
	public function get_cart_item_price( $cart ) {
		if ( ! get_option( 'vpc-license-key' ) ) {
			return;
		}
		// This is necessary for WC 3.0+ .
		if ( is_admin() && ! defined( 'DOING_AJAX' ) ) {
			return;
		}

		// Avoiding hook repetition (when using price calculations for example).
		if ( did_action( 'woocommerce_before_calculate_totals' ) >= 2 ) {
			return;
		}
		global $vpc_settings, $WOOCS; // phpcs:ignore
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );

		if ( is_array( $cart->cart_contents ) ) {
			foreach ( $cart->cart_contents as $cart_item_key => $cart_item ) {
				if ( $cart_item['variation_id'] ) {
					$product_id = $cart_item['variation_id'];
				} else {
					$product_id = $cart_item['product_id'];
				}
				$vpc_product_is_configurable = vpc_product_is_configurable( $product_id );
				if ( $vpc_product_is_configurable ) {

					$recap = get_recap_from_cart_item( $cart_item );
					if ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
						if ( vpc_woocommerce_version_check() ) {
							$cart_item['data']->price = 0;
						} else {
							$cart_item['data']->set_price( 0 );
						}
					}
					$product = wc_get_product( $product_id );

					if ( vpc_woocommerce_version_check() ) {
						$price = $cart_item['data']->price;
					} else {
						$price = $cart_item['data']->get_price();
					}

					if ( $WOOCS ) { // phpcs:ignore
						$currencies = $WOOCS->get_currencies(); // phpcs:ignore
						if ( empty( $currencies[ $WOOCS->current_currency ]['rate'] ) ) { // phpcs:ignore
							$price = null;
						} else {
							$price = $price / $currencies[ $WOOCS->current_currency ]['rate']; // phpcs:ignore
						}
					}

					if ( vpc_woocommerce_version_check() ) {
						$tax_status = $cart_item['data']->tax_status;
					} else {
						$tax_status = $cart_item['data']->get_tax_status();
					}

					$a_price = 0;
					if ( ! empty( $recap ) ) {
						$a_price = self::get_config_price( $product_id, $recap, $cart_item, true );
						if ( isset( $tax_status ) && 'taxable' !== $tax_status ) {
							$a_price = vpc_apply_taxes_on_price_if_needed( $a_price, $cart_item['data'] );
						}
					}
					if ( class_exists( 'Ofb' ) ) {
						if ( isset( $cart_item['form_data'] ) && ! empty( $cart_item['form_data'] ) ) {
							$form_data = $cart_item['form_data'];
							if ( isset( $form_data['id_ofb'] ) ) {
								$a_price += get_form_data( $form_data['id_ofb'], $recap, $product_id, true );
							}
						}
					}
					$total = vpc_get_price_before_discount( $product_id, $price ) + $a_price;
					if ( vpc_woocommerce_version_check() ) {
						$cart_item['data']->price = $total;
					} else {
						$cart_item['data']->set_price( $total );
					}
				} elseif ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
					if ( vpc_woocommerce_version_check() ) {
						$cart_item['data']->price = 0;
					} else {
						$cart_item['data']->set_price( 0 );
					}
				}
			}
		}
	}

	/**
	 * Update cart item price.
	 *
	 * @param string $price         The product price.
	 * @param array  $cart_item     The cart item.
	 * @param string $cart_item_key The cart item key.
	 * @return string
	 */
	public function update_vpc_cart_item_price( $price, $cart_item, $cart_item_key ) {
		global $vpc_settings, $WOOCS; // phpcs:ignore
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );
		if ( $cart_item['variation_id'] ) {
			$product_id = $cart_item['variation_id'];
		} else {
			$product_id = $cart_item['product_id'];
		}
		$vpc_product_is_configurable = vpc_product_is_configurable( $product_id );
		if ( $vpc_product_is_configurable ) {
			$_product = wc_get_product( $product_id );
			$price    = $_product->get_price();

			if ( vpc_woocommerce_version_check() ) {
				$tax_status = $cart_item['data']->tax_status;
			} else {
				$tax_status = $cart_item['data']->get_tax_status();
			}

			$recap = get_recap_from_cart_item( $cart_item );
			if ( ! empty( $recap ) ) {
				$a_price = self::get_config_price( $product_id, $recap, $cart_item, true );
				if ( isset( $tax_status ) && 'taxable' !== $tax_status ) {
					$a_price = vpc_apply_taxes_on_price_if_needed( $a_price, $_product );
				}
			}
			if ( class_exists( 'Ofb' ) ) {
				if ( isset( $cart_item['form_data'] ) && ! empty( $cart_item['form_data'] ) ) {
					$form_data = $cart_item['form_data'];
					if ( isset( $form_data['id_ofb'] ) ) {
						$a_price += get_form_data( $form_data['id_ofb'], $recap );
					}
				}
			}

			if ( $WOOCS ) { // phpcs:ignore
				$currencies = $WOOCS->get_currencies(); // phpcs:ignore
				if ( isset( $a_price ) && ! empty( $a_price ) ) {
					$a_price = $a_price * $currencies[ $WOOCS->current_currency ]['rate']; // phpcs:ignore
				}
			}

			if ( isset( $a_price ) && ! empty( $a_price ) ) {
				$price = $price + $a_price;
			}

			$price = wc_price( $price );
			if ( $cart_item['data']->is_on_sale() ) {
				if ( function_exists( 'vpc_get_wad_discount' ) ) {
					$base_product_price = vpc_get_wad_discount( $product_id, $_product->get_price() );
					$base_price         = $base_product_price + $a_price;
					$html               = '<del>' . ( is_numeric( $base_price ) ? wc_price( $base_price ) : $base_price ) . '</del> <ins>' . ( is_numeric( $price ) ? wc_price( $price ) : $price ) . '</ins>';
					return $html;
				}
			}
		} elseif ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
			$price = wc_price( 0 );
		}
		return $price;
	}

	/**
	 * Get configurator price.
	 *
	 * @param string $item_id          Item id.
	 * @param object $item             Item object.
	 * @param object $order            Order object.
	 */
	public function set_email_order_item_meta( $item_id, $item, $order ) {
		global $vpc_settings;
		$show_image_configured = get_proper_value( $vpc_settings, 'img-merged-mail', 'Yes' );
		$output                = '';
		$config_image          = '';
		// phpcs:ignore // if (is_order_received_page())
		// phpcs:ignore // return;
		if ( isset( $item['vpc-cart-data'] ) ) {
			$original_config = vpc_get_order_item_configuration( $item );
			if ( vpc_woocommerce_version_check() ) {
				$recap = unserialize( wp_strip_all_tags( $item['vpc-cart-data'] ) ); // phpcs:ignore
			} else {
				$recap = $item['vpc-cart-data'];
			}
			if ( ! empty( $recap ) ) {
				if ( isset( $item['vpc-custom-data']['attributes'] ) && ! empty( $item['vpc-custom-data']['attributes'] ) ) {
					$details = '';
					foreach ( $item['vpc-custom-data']['attributes'] as $key => $value ) {

						$name     = explode( '_', $key );
						$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
          <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
					}
					$output .= '<dl class="variation">' . $details . '</dl>';
				}
			}
			if ( 'Yes' === $show_image_configured ) {
				$config_image = $this->get_config_image( $recap, $original_config, $item );
			}
			$formatted_config = $this->get_formatted_config_data( $recap, $original_config, false );
			$output          .= "<style type='text/css'> .vpc-order-config img{width:150px;height:auto;margin:20px 0;}</style>
    <div class='vpc-order-config'>$config_image <div class='vpc-order-config-option'>" . $formatted_config . '</div></div>';

		}
		echo wp_kses( apply_filters( 'vpc_set_email_order', $output, $item_id, $item, $order ), get_allowed_tags() );
	}
	// @codingStandardsIgnoreStart
	/*
	  private function get_config_image_merged($recap, $config, $item) {
	  $output = "";
	  $imgs = array();
	  if (is_array($recap)) {
	  foreach ($recap as $component => $raw_options) {
	  if (is_array($raw_options)) {
	  //$options=  implode (", ", $raw_options);
	  foreach ($raw_options as $options) {
	  $image = $this->extract_option_field_from_config($options, $component, $config, "image");
	  $img_src = o_get_proper_image_url($image);
	  $title = $raw_options;
	  if (is_array($raw_options))
	  $title = implode(", ", $raw_options);
	  if ($img_src) {
	  array_push($imgs, $img_src);
	  }
	  }
	  } else {
	  $options = $raw_options;
	  $image = $this->extract_option_field_from_config($raw_options, $component, $config, "image");
	  $img_src = o_get_proper_image_url($image);
	  $title = $raw_options;
	  if (is_array($raw_options))
	  $title = implode(", ", $raw_options);
	  if ($img_src) {
	  array_push($imgs, $img_src);
	  }
	  }
	  }


	  $imgs=apply_filters('vpc_get_recap_images',$imgs, $recap, $config, $item);
	  $img_url = merge_pictures($imgs, false, true);

	  }

	  return $img_url;
	  } */
	// @codingStandardsIgnoreEnd

	/**
	 * Add class to body.
	 *
	 * @param array $classes  Configurator page body Class.
	 */
	public function add_class_to_body( $classes ) {
		$current_id   = get_the_ID();
		$configurable = vpc_product_is_configurable( $current_id );
		if ( $configurable ) {
			$classes[] = 'vpc-is-configurable';
		}

		return $classes;
	}
	// @codingStandardsIgnoreStart
	/*
	  public function set_order_again_cart_item_data($datas, $item, $order) {
	  $item_metas = $item['item_meta'];
	  $recap =array();
	  if(isset($item_metas["vpc-cart-data"])){
	  if (vpc_woocommerce_version_check())
	  $recap = unserialize($item["vpc-cart-data"]);
	  else
	  $recap = $item["vpc-cart-data"];
	  }
	  $cart_datas['visual-product-configuration']=$recap;
	  return  $cart_datas;
	  }
	 */
	// @codingStandardsIgnoreEnd

	/**
	 * Get configurator price.
	 *
	 * @param string $url           The title attribute.
	 * @param string $slug          The 2-letters language iso-code of the translation.
	 * @param string $locale        The WordPress locale for the language of the translation.
	 */
	public function get_switcher_proper_url( $url, $slug, $locale ) {
		$product_id = get_query_var( 'vpc-pid', false );
		if ( $product_id ) {
			$translation_id = icl_object_id( $product_id, 'product', true, $locale );
			$url           .= "configure/$translation_id/";
		}
		return $url;
	}

	/**
	 * Function to check product availability.
	 *
	 * @param string $product_id        The product id.
	 * @param string $quantity          The product quantity.
	 */
	public function check_product_availability( $product_id, $quantity ) {
		$product = wc_get_product( $product_id );
		$numleft = $product->get_stock_quantity();
		if ( null === $numleft || $numleft >= $quantity || $product->is_on_backorder()) {
			return true;
		} else {
			return false;
		}
	}

	/**
	 * Function to hide cart item price.
	 *
	 * @param bool   $cart_item_visible       Item visible or not.
	 * @param array  $cart_item               The cart item.
	 * @param string $cart_item_key           The cart item key.
	 * @return string
	 */
	public function hide_cart_item( $cart_item_visible, $cart_item, $cart_item_key ) {
		global $vpc_settings;
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );
		if ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
			return false;
		} else {
			return $cart_item_visible;
		}
	}

	/**
	 * Function to hide order item.
	 *
	 * @param bool   $true The cart item key.
	 * @param object $item The item object.
	 */
	public function hide_order_item( $true, $item ) {
		global $vpc_settings;
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );
		if ( isset( $item['vpc-is-secondary-product'] ) && $item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
			return false;
		} else {
			return $true;
		}
	}

	/**
	 * Function to remove secondary product.
	 *
	 * @param string $cart_item_key The cart item key.
	 */
	public function vpc_remove_secondary_products( $cart_item_key ) {
		global $woocommerce;
		if ( is_array( WC()->cart->cart_contents ) ) {
			foreach ( WC()->cart->cart_contents as $key => $values ) {
				if ( ( isset( $values['main_product_cart_item_key'] ) ) && ( ( $values['main_product_cart_item_key'] === $cart_item_key ) || ! isset( WC()->cart->cart_contents[ $values['main_product_cart_item_key'] ] ) ) ) {
					unset( WC()->cart->cart_contents[ $key ] );
				}
			}
		}
	}

	/**
	 * Function to prevent secondary product deletion.
	 *
	 * @param string $cart_item_key The cart item key.
	 */
	public function prevent_secondary_product_deletion( $cart_item_key ) {
		if ( isset( WC()->cart->cart_contents[ $cart_item_key ]['vpc-is-secondary-product'] ) && true === WC()->cart->cart_contents[ $cart_item_key ]['vpc-is-secondary-product'] ) {
			wc_add_notice( sprintf( __( 'You can not remove the secondary product', 'vpc' ) ) );
			$referer = wp_get_referer() ? remove_query_arg( array( 'undo_item', '_wpnonce' ), wp_get_referer() ) : wc_get_cart_url();
			wp_safe_redirect( $referer );
			exit;
		}
	}

	/**
	 * Allows you to filter the displayed languages of the language switcher.
	 *
	 * @param array $w_active_languages Collection of active languages to display in the language switcher.
	 */
	public function get_switcher_proper_url_wpml( $w_active_languages ) {
		$product_id     = get_query_var( 'vpc-pid', false );
		$use_pretty_url = apply_filters( 'vpc_use_pretty_url', true );
		if ( $product_id && is_array( $w_active_languages ) ) {
			foreach ( $w_active_languages as $lang => $element ) {
				$translation_id = icl_object_id( $product_id, 'product', true, $lang );
				if ( $use_pretty_url ) {
					$w_active_languages[ $lang ]['url'] .= "configure/$translation_id/";
				} else {
					$w_active_languages[ $lang ]['url'] .= "?vpc-pid=$translation_id";
				}
			}
		}
		return $w_active_languages;
	}

	/**
	 * Get vpc product quantity ajax.
	 */
	public function get_vpc_product_qty_ajax() {
		$prod_id               = $_POST['prod_id']; // phpcs:ignore
		$_COOKIE['attributes'] = $_POST['new_variation_attributes']; // phpcs:ignore
		$qty                   = $_POST['qty']; // phpcs:ignore
		$design_url            = vpc_get_configuration_url( $prod_id );
		if ( $qty > 1 ) {
			$design_url = add_query_arg( 'qty', $qty, $design_url );
		}
		apply_filters( 'vpc_get_product_qty_ajax', $design_url, $_POST ); // phpcs:ignore
		echo esc_url( $design_url );
		die();
	}

	/**
	 * Get configurator details.
	 *
	 * @param string $item_id          Item id.
	 * @param object $item             Item object.
	 * @param object $order            Order object.
	 */
	public function get_vpc_config_details( $item_id, $item, $order ) {
		$output          = '';
		$original_config = vpc_get_order_item_configuration( $item );
		$output         .= '<br>';
		if ( ! is_array( $item['vpc-cart-data'] ) ) {
			$recap = unserialize( $item['vpc-cart-data'] ); // phpcs:ignore
		} else {
			$recap = $item['vpc-cart-data'];
		}

		if ( ! empty( $recap ) ) {
			if ( isset( $item['vpc-custom-data']['attributes'] ) && ! empty( $item['vpc-custom-data']['attributes'] ) ) {
				$details = '';
				foreach ( $item['vpc-custom-data']['attributes'] as $key => $value ) {

					$name     = explode( '_', $key );
					$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
        <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
				}
				$output .= '<dl class="variation">' . $details . '</dl>';
			}
		}
		$formatted_config = self::get_formatted_config_data( $recap, $original_config, false );
		$output          .= "<div class='vpc-order-config o-wrap xl-gutter-8'><div class='o-col xl-2-3'>" . $formatted_config . '</div></div>';
		echo wp_kses( $output, get_allowed_tags() );
	}

	/**
	 * Get form builder data.
	 *
	 * @param array $form_data    Form builder datas.
	 */
	public function get_form_build_data( $form_data ) {
		$form_html = '<strong>Your form data</strong><br>';
		foreach ( $form_data as $index => $data ) {
			if ( is_array( $data ) ) {
				foreach ( $data as $opt => $opt_data ) {
					$form_html .= $index . ' :<br>' . $opt . ' :' . $opt_data . '<br>';
				}
			} else {
				if ( 'id_ofb' === $index ) {
					$form_html .= ' ';
				} elseif ( ! empty( $data ) ) {
					$form_html .= $index . ' :' . $data . '<br>';
				}
			}
		}
		return $form_html;
	}

	/**
	 * Function to update price from form
	 */
	public function update_price_from_form() {
		if ( isset( $_POST['form_data'] ) ) { // phpcs:ignore
			$form_data = $_POST['form_data']; // phpcs:ignore
			$form_id   = $form_data['id_ofb'];
			$price     = get_form_data( $form_data['id_ofb'], $form_data );
		}
		echo esc_html( $price );
		die();
	}

	/**
	 * Function to update number of items in the cart.
	 *
	 * @param int $cart_item_count Number of items in the cart.
	 * @return int
	 */
	public function update_cart_contents_count( $cart_item_count ) {
		global $vpc_settings;
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart' );
		if ( 'Yes' === $hide_secondary_product_in_cart && is_array( WC()->cart->cart_contents ) ) {
			foreach ( WC()->cart->cart_contents as $key => $items ) {
				if ( isset( $items['vpc-is-secondary-product'] ) ) {
					$quantity        = $items['quantity'];
					$cart_item_count = $cart_item_count - $quantity;
				}
			}
		}
		return $cart_item_count;
	}

	/**
	 * Set invoice order item.
	 *
	 * @param string $product          Product object.
	 * @param object $order            Order object.
	 * @param object $item             Item object.
	 */
	public function set_invoice_order_item_meta( $product, $order, $item ) {
		global $vpc_settings;
		$output = '';

		if ( isset( $item['vpc-cart-data'] ) ) {
			$original_config = vpc_get_order_item_configuration( $item );
			if ( vpc_woocommerce_version_check() ) {
				$recap = unserialize( wp_strip_all_tags( $item['vpc-cart-data'] ) ); // phpcs:ignore
			} else {
				$recap = $item['vpc-cart-data'];
			}
			if ( ! empty( $recap ) ) {
				if ( isset( $item['vpc-custom-data']['attributes'] ) && ! empty( $item['vpc-custom-data']['attributes'] ) ) {
					$details = '';
					foreach ( $item['vpc-custom-data']['attributes'] as $key => $value ) {

						$name     = explode( '_', $key );
						$details .= '<dt class="variation-' . ucfirst( end( $name ) ) . '">' . ucfirst( end( $name ) ) . ':</dt>
          <dd class="variation-' . ucfirst( end( $name ) ) . '"><p>' . ucfirst( $value ) . '</p></dd>';
					}
					$output .= '<dl class="variation">' . $details . '</dl>';
				}
			}
			$config_image = $this->get_config_image( $recap, $original_config, $item );

			$formatted_config = $this->get_formatted_config_data( $recap, $original_config, false );
			$output          .= "<style type='text/css'> .vpc-order-config img{width:150px;height:auto;margin:20px 0;}</style>
    <div class='vpc-order-config'>$config_image <div class='vpc-order-config-option'>" . $formatted_config . '</div></div>';
		}

		echo wp_kses( $output, get_allowed_tags() );
	}

	/**
	 * Function to set wad variable is_applicable if the discount i applicable on the product
	 *
	 * @param string $is_valid   The discount validity.
	 * @param object $wad        The discount object.
	 * @param string $product_id The product id.
	 */
	public function check_if_wad_is_applicable( $is_valid, $wad, $product_id ) {
		if ( false !== $wad->get_products_list()->get_products( true ) ) {
			if ( in_array( $product_id, $wad->get_products_list()->get_products( true ), true ) ) {
				return true;
			}
		}
		return false;
	}

	/**
	 * Function to set wad variable is_applicable if the discount i applicable on the product
	 *
	 * @param string $sale_price            The product sale price.
	 * @param string $original_sale_price   The original sale price.
	 * @param object $product               The object object.
	 */
	public function get_sale_price_if_linkedd_product_is_hide( $sale_price, $original_sale_price, $product ) {
		global $woocommerce, $vpc_settings, $wad_discounts;
		$items                          = $woocommerce->cart->get_cart();
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart', 'Yes' );

		$product_id = $product->get_id();

		foreach ( $items as $item => $cart_item ) {
			if ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
				if ( $product_id === $cart_item['product_id'] ) {
					$sale_price = 0;
				}
			} elseif ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'No' === $hide_secondary_product_in_cart ) {
				if ( $product_id === $cart_item['product_id'] ) {
					foreach ( $wad_discounts['product'] as $discount_id => $discount_obj ) {
						if ( $discount_obj->is_applicable( $product_id ) ) {
							$sale_price = $sale_price;
						} else {
							$product    = wc_get_product( $product_id );
							$price      = $product->get_regular_price();
							$sale_price = $price - $discount_obj->get_discount_amount( $price );
						}
					}
				}
			}
		}
		return $sale_price;
	}

	/**
	 * Show the original price on cart
	 *
	 * @param string $formatted_price  The formated current price on the cart.
	 * @param array  $cart_item        The current cart item.
	 * @return string
	 */
	public function show_original_price_on_cart( $formatted_price, $cart_item ) {
		global $vpc_settings;
		$hide_secondary_product_in_cart = get_proper_value( $vpc_settings, 'hide-wc-secondary-product-in-cart' );

		if ( $cart_item['data']->is_on_sale() ) {
			if ( $cart_item['variation_id'] ) {
				$product_id = $cart_item['variation_id'];
			} else {
				$product_id = $cart_item['product_id'];
			}

			$recap = get_recap_from_cart_item( $cart_item );
			if ( isset( $cart_item['vpc-is-secondary-product'] ) && $cart_item['vpc-is-secondary-product'] && 'Yes' === $hide_secondary_product_in_cart ) {
				if ( vpc_woocommerce_version_check() ) {
					$cart_item['data']->price = 0;
				} else {
					$cart_item['data']->set_price( 0 );
				}
			}

			$product = wc_get_product( $product_id );
			if ( vpc_woocommerce_version_check() ) {
				$price = $cart_item['data']->price;
			} else {
				$price = $cart_item['data']->get_price();
			}

			$a_price = 0;
			if ( ! empty( $recap ) ) {
				$a_price = self::get_config_price( $product_id, $recap, $cart_item, false );
				if ( isset( $tax_status ) && 'taxable' !== $tax_status ) {
					$a_price = vpc_apply_taxes_on_price_if_needed( $a_price, $cart_item['data'] );
				}
			}
			if ( class_exists( 'Ofb' ) ) {
				if ( isset( $cart_item['form_data'] ) && ! empty( $cart_item['form_data'] ) ) {
					$form_data = $cart_item['form_data'];
					if ( isset( $form_data['id_ofb'] ) ) {
						$a_price += get_form_data( $form_data['id_ofb'], $recap, $product_id, false );
					}
				}
			}
			if ( function_exists( 'vpc_get_wad_discount' ) ) {
				$base_product_price = $product->get_regular_price();
				$base_product_price = vpc_get_wad_discount( $product_id, $base_product_price );
				$base_price         = $base_product_price + $a_price;
				$html               = '<del>' . ( is_numeric( $base_price ) ? wc_price( $base_price ) : $base_price ) . '</del> <ins>' . ( is_numeric( $price ) ? wc_price( $price ) : $price ) . '</ins>';
				return $html;
			}
			// phpcs:ignore // $total = $product->get_regular_price() + $a_price;
			// phpcs:ignore // $formatted_price = '<del>' . ( is_numeric( $total ) ? wc_price( $total ) : $total ) . '</del> <ins>' . ( is_numeric( $price ) ? wc_price( $price ) : $price ) . '</ins>';
		}
		return $formatted_price;
	}

	/**
	 * Calculate mini cart sub cart total.
	 */
	public function calculate_minicart_subcartotal() {
		WC()->cart->calculate_totals();
	}

	/**
	 * Hide secondary product item meta
	 *
	 * @param string $html Product display content.
	 * @param type   $item Cart item.
	 * @param type   $args  Argument array.
	 * @return string
	 */
	public function hide_secondary_product_item_meta( $html, $item, $args ) {
		if ( isset( $item['vpc-is-secondary-product'] ) ) {
			$html = '';
		}
		return $html;
	}

	/**
	 *  add custom class on the  configurable products on cart page
	 * @param type   $class class.
	 * @param type   $cart_item Cart item.
	 * @param type   $cart_item_key item key.
	 * @return string
	 */
	function add_vpc_classes_on_cart_item($class, $cart_item ,$cart_item_key){
		if ( $cart_item['variation_id'] ) {
			$product_id = $cart_item['variation_id'];
		} else {
			$product_id = $cart_item['product_id'];
		}
		$vpc_product_is_configurable = vpc_product_is_configurable( $product_id );
		if ( $vpc_product_is_configurable ) 
		$class.=" is-configurable";
		return $class;
	}
}
