<?php
if ( !defined('ABSPATH') ) {
	exit;
}
if ( !function_exists('pbq_pricing_vertical_table') ) {
	function pbq_pricing_vertical_table( $product, $pricing_table ) { 
		$qty_label = get_option('pbq_quantity_pricing_qty_label');
		$qty_label = !empty($qty_label)  ? esc_html__($qty_label, 'price-by-quantity') : esc_html__('Quantity', 'price-by-quantity');
		$max_qty = get_post_meta($product->get_id(), 'pbq_max_quantity', true);
		?>
		<table>
			<tr>
				<th><?php esc_html_e($qty_label); ?></th>
			<?php
			$pricing_type = !empty($pricing_table['pricing_type']) ? $pricing_table['pricing_type'] : 'fixed';
			$discount_table = !empty($pricing_table['discount_table']) ? $pricing_table['discount_table'] : array();
			foreach ( $discount_table as $key => $table) {
				$qty = !empty( $table['pbq_quantity'] ) ? $table['pbq_quantity'] : 1;
				$qty_next = isset($discount_table[$key+1]) ? $discount_table[$key+1]['pbq_quantity'] : ''; 
				?>
					<td class="pbq_choose_quantity" data-current="<?php echo esc_attr($qty); ?>">
						<?php 
						if ( !empty($qty_next) ) {
							if ( empty(get_option('pbq_pricing_table_quantities_display')) ) {
								printf('%s %s %s', esc_html($qty), ' - ', esc_html($qty_next-1));
							} else {
								printf('%s', esc_html($qty));
							}
						} else {
							if ( $max_qty > $qty  ) {
								printf('%s %s', esc_html($qty), ' + ');
							} else {
								printf('%s', esc_html($qty));
							}
						} 
						?>
					</td>
			<?php } ?>
			</tr>
			<tr>
			<?php
			$pricing_label = get_option('pbq_quantity_pricing_price_label');
			$pricing_label = !empty($pricing_label) ? esc_html__($pricing_label, 'price-by-quantity') : esc_html__('Price', 'price-by-quantity'); 
			?>
				<th><?php esc_html_e($pricing_label); ?></th>
			<?php
			$pricing_type = !empty($pricing_table['pricing_type']) ? $pricing_table['pricing_type'] : 'fixed';
			$discount_table = !empty($pricing_table['discount_table']) ? $pricing_table['discount_table'] : array();
			foreach ( $discount_table as $key => $table) {
				$discount = !empty( $table['pbq_discount'] ) ? $table['pbq_discount'] : 0;
				$discounted_price = pbq_calculate_discounted_price($product, $discount, $pricing_type);
				$qty = !empty( $table['pbq_quantity'] ) ? $table['pbq_quantity'] : 1;
				$qty_next = isset($discount_table[$key+1]) ? $discount_table[$key+1]['pbq_quantity'] : ''; 
				?>
					<td class="pbq_pricing_tr pbq_choose_quantity" data-next="<?php echo esc_attr($qty_next); ?>" data-current="<?php echo esc_attr($qty); ?>" data-discount_price="<?php echo esc_attr($discounted_price); ?>">
					<?php echo wp_kses_post(wc_price($discounted_price)); ?>
					</td>
			<?php } ?>
			</tr>
		</table>
		<?php
	}
}
if ( !function_exists('pbq_pricing_table_rows') ) {
	function pbq_pricing_table_rows( $product, $pricing_table ) { 
		$max_qty = get_post_meta($product->get_id(), 'pbq_max_quantity', true);
		$pricing_type = !empty($pricing_table['pricing_type']) ? $pricing_table['pricing_type'] : 'fixed';
		$discount_table = !empty($pricing_table['discount_table']) ? $pricing_table['discount_table'] : array();
		?>
		<table>
			<tr>
				<?php
				$qty_label = get_option('pbq_quantity_pricing_qty_label');
				$qty_label = !empty($qty_label)  ? esc_html__($qty_label, 'price-by-quantity') : esc_html__('Quantity', 'price-by-quantity');
				$pricing_label = get_option('pbq_quantity_pricing_price_label');
				$pricing_label = !empty($pricing_label)  ? esc_html__($pricing_label, 'price-by-quantity') : esc_html__('Price', 'price-by-quantity'); 
				?>
				<th colspan="<?php echo esc_attr(count($discount_table)); ?>"><?php printf('%s %s', esc_html($qty_label), esc_html($pricing_label)); ?></th>
			</tr>
			<tr>
				<?php
				foreach ( $discount_table as $key => $table) {
					$qty = !empty( $table['pbq_quantity'] ) ? $table['pbq_quantity'] : 1;
					$qty_next = isset($discount_table[$key + 1]) ? $discount_table[$key + 1]['pbq_quantity'] : '';
					$discount = !empty( $table['pbq_discount'] ) ? $table['pbq_discount'] : 0;
					$discounted_price = pbq_calculate_discounted_price($product, $discount, $pricing_type); 
					?>
					<td class="pbq_pricing_tr pbq_choose_quantity" data-next="<?php echo esc_attr($qty_next); ?>" data-current="<?php echo esc_attr($qty); ?>" data-discount_price="<?php echo esc_attr($discounted_price); ?>">
						<?php
						if ( !empty($qty_next) ) {
							if ( empty(get_option('pbq_pricing_table_quantities_display')) ) {
								// printf('%s %s %s', esc_html($qty), ' - ', esc_html($qty_next-1));
								// GIL change
								printf('%s', esc_html($qty));
							} else {
								printf('%s', esc_html($qty));
							}
						} else {
							if ( $max_qty > $qty  ) {
								printf('%s %s', esc_html($qty), ' + ');
							} else {
								printf('%s', esc_html($qty));
							}
						} 
						?>
					</td>
				<?php } ?>
			</tr>
			<tr>
				<?php
				$pricing_type = !empty($pricing_table['pricing_type']) ? $pricing_table['pricing_type'] : 'fixed';
				$discount_table = !empty($pricing_table['discount_table']) ? $pricing_table['discount_table'] : array();
				foreach ( $discount_table as $key => $table) {
					$discount = !empty( $table['pbq_discount'] ) ? $table['pbq_discount'] : 0;
					$discounted_price = pbq_calculate_discounted_price($product, $discount, $pricing_type);
					?>
					<td><?php echo wp_kses_post(wc_price($discounted_price)); ?></td>
				<?php } ?>
			</tr>
		</table>
		<?php
	}
}
if ( !function_exists('pbq_pricing_horizontal_table') ) {
	function pbq_pricing_horizontal_table( $product, $pricing_table ) {
			$max_qty = get_post_meta($product->get_id(), 'pbq_max_quantity', true);
		?>
		<table>
			<tr>
				<?php
				$qty_label = get_option('pbq_quantity_pricing_qty_label');
				$qty_label = !empty($qty_label)  ? esc_html__($qty_label, 'price-by-quantity') : esc_html__('Quantity', 'price-by-quantity');
				$discount_label = get_option('pbq_quantity_pricing_discount_label');
				$discount_label = !empty($discount_label)  ? esc_html__($discount_label, 'price-by-quantity') : esc_html__('Discount', 'price-by-quantity');
				$pricing_label = get_option('pbq_quantity_pricing_price_label');
				$pricing_label = !empty($pricing_label)  ? esc_html__($pricing_label, 'price-by-quantity') : esc_html__('Price', 'price-by-quantity'); 
				$hide_discount_column = get_option('pbq_pricing_table_hide_discount_column');
				?>
				<th><?php esc_html_e($qty_label); ?></th>
				<?php if ( !$hide_discount_column ) { ?>
				<th><?php esc_html_e($discount_label); ?></th>
				<?php } ?>
				<th><?php esc_html_e($pricing_label); ?></th>
			</tr>
			<?php
			$pricing_type = !empty($pricing_table['pricing_type']) ? $pricing_table['pricing_type'] : 'fixed';
			$discount_table = !empty($pricing_table['discount_table']) ? $pricing_table['discount_table'] : array();
			foreach ( $discount_table as $key => $table) {
				$qty = !empty( $table['pbq_quantity'] ) ? $table['pbq_quantity'] : 1;
				$qty_next = isset($discount_table[$key+1]) ? $discount_table[$key+1]['pbq_quantity'] : '';
				$discount = !empty( $table['pbq_discount'] ) ? $table['pbq_discount'] : 0;
				$discounted_price = pbq_calculate_discounted_price($product, $discount, $pricing_type); 
				?>
				<tr class="pbq_pricing_tr pbq_choose_quantity" data-next="<?php echo esc_attr($qty_next); ?>" data-current="<?php echo esc_attr($qty); ?>" data-discount_price="<?php echo esc_attr($discounted_price); ?>">
					<td>
						<?php 
						if ( !empty($qty_next) ) {
							if ( empty(get_option('pbq_pricing_table_quantities_display')) ) {
								// printf('%s %s %s', esc_html($qty), ' - ', esc_html($qty_next-1));
								// GIL change
								printf('%s', esc_html($qty));
							} else {
								printf('%s', esc_html($qty));
							}
						} else {
							if ( $max_qty > $qty  ) {
								printf('%s %s', esc_html($qty), ' + ');
							} else {
								printf('%s', esc_html($qty));
							}
						} 
						?>
					</td>
					<?php if ( !$hide_discount_column ) { ?>
					<td>
						<?php
						if ( 'fixed' == $pricing_type ) {
							echo wp_kses_post(wc_price($discount));
						} else {
							printf('%s%s', esc_html($discount), '%');
						} 
						?>
					</td>
					<?php } ?>
					<td><?php echo wp_kses_post(wc_price($discounted_price)); ?></td>
				</tr>
				<?php } ?>
		</table>
		<?php
	}
}
if ( !function_exists('pbq_calculate_discounted_price') ) {
	function pbq_calculate_discounted_price( $product, $discount, $pricing_type) {
		$discounted_price = 0;
		$product_price = $product->get_price();
		if ( !empty($product->get_tax_status()) && 'none' != $product->get_tax_status() ) {
			if ( 'yes' == get_option('woocommerce_prices_include_tax') ) {
				$product_price = wc_get_price_excluding_tax($product);
			}
		}
		if ( 'fixed' == $pricing_type ) {
			$discounted_price = $product_price - $discount;
		} else {
			if ( empty($discount) ) {
				return $product_price;
			}
			$discount_percentage_val = ( $discount / 100 );
			$discount_value = ( $product_price * $discount_percentage_val );
			$discounted_price = $product_price - $discount_value;
		}
		return $discounted_price;
	}
}
if ( !function_exists('pbq_pricing_table_status') ) {
	function pbq_pricing_table_status( $product_id ) {
		$table_data = array();
		$product = wc_get_product($product_id);
		$pricing_status = get_post_meta($product_id, 'pbq_pricing_type_enable', true);
		if ( 'disable' == $pricing_status ) {
			return false;
		} else if ( 'enable' == $pricing_status ) {
			$pricing_type = get_post_meta( $product_id, 'pbq_pricing_type', true);
			$discount_table = get_post_meta( $product_id, 'pbq_discount_table_data', true);
			$table_style = get_post_meta( $product_id, 'pbq_table_layout', true);
			$min = get_post_meta($product_id, 'pbq_min_quantity', true);
			$max = get_post_meta($product_id, 'pbq_max_quantity', true);
			return array( 'pricing_type' => $pricing_type, 'discount_table' => $discount_table, 'table_style' => $table_style, 'min' => $min, 'max' => $max );
		} else {
			if ( $product->is_type('variation') ) {
				$product_id = wp_get_post_parent_id($product_id);
			}
			$terms = get_the_terms ( $product_id, 'product_cat' );
			if ( !is_wp_error($terms) && !empty($terms) ) {
				foreach ( $terms as $term ) {
					$cat_pricing = get_term_meta($term->term_id, 'pbq_pricing_type_enable', true);
					if ( 'yes' == $cat_pricing ) {
						$discount_table = get_term_meta($term->term_id, 'pbq_discount_table_data', true);
						$pricing_type = get_term_meta($term->term_id, 'pbq_pricing_type', true);
						$table_style = get_term_meta( $term->term_id, 'pbq_table_layout', true);
						$min = get_term_meta($term->term_id, 'pbq_min_quantity', true);
						$max = get_term_meta($term->term_id, 'pbq_max_quantity', true);
						return array( 'pricing_type' => $pricing_type, 'discount_table' => $discount_table, 'table_style' => $table_style, 'min' => $min, 'max' => $max );
					} else {
						continue;
					}
				}
			}
		}
		return false;
	}
}
if ( !function_exists('pbq_pricing_table') ) {
	function pbq_pricing_table( $product_id, $status = '' ) {
		$product = wc_get_product($product_id);
		$pricing_table = pbq_pricing_table_status($product_id);
		if ( !empty($pricing_table['discount_table']) ) {
			ob_start();
			$table_style = !empty($pricing_table['table_style']) ? $pricing_table['table_style'] : ''; 
			?>
			<div class="pbq_quantity_pricing_tables">
			<?php 
			if ( !get_option('pbq_hide_pricing_table') || 'shortcode' === $status ) { 
				?>
			<div class="pbq_pricing_table">
				<?php 
				$before_table = get_option('pbq_quantity_content_before_pricing_table');
				echo wp_kses_post($before_table);
				if ( 'vertical' == $table_style ) {
					pbq_pricing_vertical_table($product, $pricing_table);
				} else if ( 'hover_table' == $table_style ) {
					pbq_pricing_horizontal_table($product, $pricing_table);
				} else {
					pbq_pricing_table_rows($product, $pricing_table);
				}
				$after_table = get_option('pbq_quantity_content_after_pricing_table');
				echo wp_kses_post($after_table); 
				?>
			</div>
				<?php 
			}
			?>
			</div>
			<?php
			return ob_get_clean();
		}
	}
}
if ( !function_exists('pbq_summary_table') ) {
	function pbq_summary_table( $product_id, $status = '' ) {
		if ( 'yes' == get_option('pbq_hide_pricing_summary') && empty($status) ) { 
			return;
		}
		$pricing_table = pbq_pricing_table_status($product_id);
		if ( empty($pricing_table['discount_table']) ) {
			return;
		}
		ob_start();
		$product = wc_get_product($product_id);
		$product_price = $product->get_price();
		$summary = get_option('pbq_summary_label');
		$summary = !empty($summary) ? __($summary, 'price-by-quantity') : __('Summary', 'price-by-quantity');
		?>
		<div class="pbq_pricing_summary">
			<table>
				<tr><th><?php esc_html_e($summary); ?></th><th></th></tr>
				<tr><td><?php esc_html_e( $product->get_name() ); ?></td><td class="pbq_product_price" data-product_price="<?php echo esc_attr( $product_price ); ?>"><?php echo wp_kses_post( $product->get_price_html() ); ?></td></tr>
				<tr><td class="pbq_qty_added"></td><td class="pbq_total_price"><?php echo wp_kses_post($product->get_price_html()); ?></td></tr>
			</table>
		</div>
		<?php 
		return ob_get_clean();
	}
}
