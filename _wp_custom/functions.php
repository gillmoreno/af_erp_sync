<?php

//add_filter( 'woocommerce_hide_invisible_variations', '__return_true' );
//
//

function current_user_id()
{

    $id = get_current_user_id();
    return $id;

}
add_shortcode('current_user_id', 'current_user_id');

// API FOR CLICHE
class Cliche_API_Controller extends WP_REST_Controller {
    public function cliche_callback( $request ) {
		$image_id = $request['image_id'];
        $user_id = $request['customer_id'];
		$post_content = $request['post_content'];
		
		$cliche = array(
			'ID' => $image_id,
			'post_author' => $user_id,
			'post_content' => $post_content
		);
		$result = wp_update_post( $cliche );
		
        $data = [
			'image_id' => $image_id,
			'user_id' => $user_id,
			'post_content' => $post_content,
			'cliche' => $result
			
        ];
        return rest_ensure_response( $data );
    }
}

add_action( 'rest_api_init', function () {
    $namespace = 'wp-api/v1';
    $route = '/cliche';
    $args = [
        'methods' => 'GET',
        'callback' => [ new Cliche_API_Controller(), 'cliche_callback' ],
    ];
    register_rest_route( $namespace, $route, $args );
} );

//API FOR MEDIA GALLERY

add_action('rest_api_init', 'register_rest_images');
function register_rest_images()
{
    register_rest_field(
        'post',
        'featured_image_src',
        array(
            'get_callback' => 'get_image_src',
            'update_callback' => null,
            'schema' => null,
        )
    );
}
function get_image_src($object, $field_name, $request)
{
    if ($object['featured_media']) {
        $img = wp_get_attachment_image_src($object['featured_media'], 'app-thumb');
        return $img[0];
    }
    return false;
}

//Register taxonomy API for WC
add_action('rest_api_init', 'register_rest_field_for_images');
function register_rest_field_for_images()
{

    register_rest_field('product', "image", array(
        'get_callback' => 'product_get_callback',
        'update_callback' => 'product_update_callback',
        'scheme' => null
    )
    );

    register_rest_route('wc/v3', 'image', array(
        'methods' => 'GET',
        'callback' => 'get_image_id_by_name',
    )
    );

}

function get_image_id_by_name($data)
{
    $params = $data->get_query_params();
    $image_name = $params['image_name'];
    $args = array(
        'post_type' => 'attachment',
        'post_status' => 'inherit',
        'posts_per_page' => 1,
        'name' => trim($image_name),
    );

    $query = new WP_Query($args);
    if ($query->have_posts()) {
        $query->the_post();
        return get_the_ID();
    } else {
        return 0;
    }
}

//Register taxonomy API for WC
add_action('rest_api_init', 'register_rest_field_for_custom_taxonomy_brands');
function register_rest_field_for_custom_taxonomy_brands()
{

    register_rest_field('product', "brand", array(
        'get_callback' => 'product_get_callback',
        'update_callback' => 'product_update_callback',
        'scheme' => null
    )
    );

    register_rest_route('wc/v3', 'brand', array(
        'methods' => 'GET',
        'callback' => 'get_brand',
    )
    );

    register_rest_route('wc/v3', 'create-brand', array(
        'methods' => 'GET',
        'callback' => 'create_brand',
    )
    );

    register_rest_route('wc/v3', 'relate-brand', array(
        'method' => 'GET',
        'callback' => 'relate_brand',
    )
    );

}

// INPUT PRODUCT ID
function get_brand($data)
{
    $taxonomy = 'brand';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $product_id_en = apply_filters('wpml_object_id', $product_id, 'product', FALSE, 'en');
    foreach (wp_get_post_terms($product_id, $taxonomy) as $term) {
        $terms[] = array(
            'id' => $term->term_id,
            'name' => $term->name,
            'slug' => $term->slug,
        );
    }

    foreach (wp_get_post_terms($product_id_en, $taxonomy) as $term) {
        $terms[] = array(
            'id' => $term->term_id,
            'name' => $term->name,
            'slug' => $term->slug,
        );
    }

    return $terms;
}

// INPUT PRODUCT ID, VALUE
function create_brand($data)
{

    $taxonomy = 'brand';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $product_id_en = apply_filters('wpml_object_id', $product_id, 'product', FALSE, 'en');
    $value = $params['brand_name'];

    $new_term = wp_insert_term($value, $taxonomy, array('slug' => $value));
    wp_set_object_terms($product_id, $new_term['term_id'], $taxonomy);

    $new_term_en = wp_insert_term($value, $taxonomy, array('slug' => $value . '-en'));
    wp_set_object_terms($product_id_en, $new_term_en['term_id'], $taxonomy);

    $trid = wpml_get_content_trid('tax_' . $taxonomy, $new_term['term_id']);

    // Associate original term and translated term
    global $wpdb;
    $wpdb->update($wpdb->prefix . 'icl_translations', array('trid' => $trid, 'language_code' => 'en', 'source_language_code' => 'it'), array('element_id' => $new_term_en['term_id'], 'element_type' => 'tax_' . $taxonomy));

    return [$new_term, $new_term_en];
}

// INPUT PRODUCT ID, BRAND ID
function relate_brand($data)
{

    $taxonomy = 'brand';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $term_id = $params['brand_id'];

    return wp_set_object_terms($product_id, (int) $term_id, $taxonomy);
}


add_action('rest_api_init', 'register_rest_field_for_custom_taxonomy_colors');
function register_rest_field_for_custom_taxonomy_colors()
{

    register_rest_field('product', "color", array(
        'get_callback' => 'product_get_callback',
        'update_callback' => 'product_update_callback',
        'schema' => null,
    )
    );

    register_rest_route('wc/v3', 'color', array(
        'methods' => 'GET',
        'callback' => 'get_color',
    )
    );

    register_rest_route('wc/v3', 'create-color', array(
        'methods' => 'GET',
        'callback' => 'create_color',
    )
    );

    register_rest_route('wc/v3', 'relate-color', array(
        'method' => 'GET',
        'callback' => 'relate_color',
    )
    );

}

// INPUT PRODUCT ID
function get_color($data)
{
    $taxonomy = 'colore';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $product_id_en = apply_filters('wpml_object_id', $product_id, 'product', FALSE, 'en');
    foreach (wp_get_post_terms($product_id, $taxonomy) as $term) {
        $terms[] = array(
            'id' => $term->term_id,
            'name' => $term->name,
            'slug' => $term->slug,
        );
    }

    foreach (wp_get_post_terms($product_id_en, $taxonomy) as $term) {
        $terms[] = array(
            'id' => $term->term_id,
            'name' => $term->name,
            'slug' => $term->slug,
        );
    }

    return $terms;
}

// INPUT PRODUCT ID, VALUE IT, VALUE EN
function create_color($data)
{

    $taxonomy = 'colore';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $product_id_en = apply_filters('wpml_object_id', $product_id, 'product', FALSE, 'en');
    $value_it = $params['color_name'];
    $value_en = $params['color_name_en'];

    $new_term = wp_insert_term($value_it, $taxonomy, array('slug' => $value_it));
    wp_set_object_terms($product_id, $new_term['term_id'], $taxonomy, true);

    $new_term_en = wp_insert_term($value_en, $taxonomy, array('slug' => $value_en . '-en'));
    wp_set_object_terms($product_id_en, $new_term_en['term_id'], $taxonomy, true);

    $trid = wpml_get_content_trid('tax_' . $taxonomy, $new_term['term_id']);

    // Associate original term and translated term
    global $wpdb;
    $wpdb->update($wpdb->prefix . 'icl_translations', array('trid' => $trid, 'language_code' => 'en', 'source_language_code' => 'it'), array('element_id' => $new_term_en['term_id'], 'element_type' => 'tax_' . $taxonomy));

    return [$new_term, $new_term_en];
}

// INPUT PRODUCT ID, COLOR ID
function relate_color($data)
{

    $taxonomy = 'colore';
    $params = $data->get_query_params();
    $product_id = $params['product_id'];
    $term_id = $params['color_id'];

    return wp_set_object_terms($product_id, (int) $term_id, $taxonomy, true);
}

//___________________END API_________________

add_action("wpcf7_before_send_mail", "wpcf7_admin_email");

function wpcf7_admin_email($WPCF7_ContactForm)
{
    //Get current form
    $wpcf7 = WPCF7_ContactForm::get_current();
    $contact_form_id = $wpcf7->id;
    if ($contact_form_id === 107 || $contact_form_id === 2690) {

        // get current SUBMISSION instance
        $submission = WPCF7_Submission::get_instance();
        $email = $submission->get_posted_data('email');
        $user = get_user_by('email', $email);
        // Ok go forward
        if ($submission) {
            // get submission data
            $data = $submission->get_posted_data();
            // nothing's here... do nothing...
            if (empty($data)) {
                return;
            }

            $mail = $wpcf7->prop('mail');
            
            $hashed_id = wp_hash($user->ID);
    		update_user_meta($user->ID, 'hashed_id', $hashed_id);

            $ua_links = '<a target="_blank" href="https://' . $_SERVER['HTTP_HOST'] . '/ua.php?action=approved&id=' . $hashed_id . '">Approva</a>' . '<br><a target="_blank" href="https://' . $_SERVER['HTTP_HOST'] . '/ua.php?action=denied&id=' . $hashed_id . '">Rifiuta</a>';

            $end_body = ' -- <br>
					Questa e-mail è stata inviata dal modulo di registrazione su [_site_title] ([_site_url])';

            $mail['body'] = $mail['body'] . '<br><br>' . $ua_links . '<br>' . $end_body;

            // Save the email body
            $wpcf7->set_properties(
                array(
                    "mail" => $mail
                )
            );
            // return current cf7 instance
            return $wpcf7;
        }
    }
}

function console_log($output, $with_script_tags = true)
{
    $js_code = 'console.log(' . json_encode($output, JSON_HEX_TAG) . ');';
    if ($with_script_tags) {
        $js_code = '<script>' . $js_code . '</script>';
    }
    echo $js_code;
}

// REGISTRAZIONE - disabilitare invio default email dopo registrazione
if (class_exists('pw_new_user_approve')) {

    add_action('init', 'remove_approve_email_hook');
}

function remove_approve_email_hook()
{
    $myclass = pw_new_user_approve();
    remove_action('user_register', array($myclass, 'request_admin_approval_email_2'));
}

// REGISTRAZIONE - controllo Partita IVA prima dell'invio della richiesta
function verificaPIVA($piva) {
  if (strlen($piva) != 11) {
    return false;
  }
  if (!is_numeric($piva)) {
    return false;
  }
  $s = 0;
  for ($i = 0; $i <= 9; $i += 2) {
    $s += ord($piva[$i]) - ord('0');
  }
  for ($i = 1; $i <= 9; $i += 2) {
    $c = 2 * (ord($piva[$i]) - ord('0'));
    if ($c > 9) {
      $c = $c - 9;
    }
    $s += $c;
  }
  $checkdigit = (10 - ($s % 10)) % 10;
  return ($checkdigit == ord($piva[10]) - ord('0'));
}

add_filter('wpcf7_validate', 'verifica_piva_cf7', 10, 2);

function verifica_piva_cf7( $result ) {
  $submission = WPCF7_Submission::get_instance();
  if ( $submission ) {
    $piva = $submission->get_posted_data('vat-number');
    if ( !verificaPIVA( $piva ) ) {
      $result->invalidate('vat-number', 'Partita IVA non valida');
    }
  }
  return $result;
}

// REGISTRAZIONE - check se l'utente è già nel DB
add_filter('wpcf7_validate', 'email_already_in_db', 10, 2);

function email_already_in_db($result)
{
    // retrieve the posted email
    $form = WPCF7_Submission::get_instance();
    $email = $form->get_posted_data('email');
    // if already in database, invalidate
    if (email_exists($email)) // email_exists is a WP function
        $result->invalidate('email', 'Your email exists in our database');
    // return the filtered value
    return $result;
}

// REGISTRAZIONE - new user approve mail message
add_filter('new_user_approve_approve_user_message', function ($message, $user) {

    add_filter('wp_mail_content_type', function ($content_type) {
        $content_type = 'text/html';
        return $content_type;
    }
    );
    $username = $user->data->user_login;

    $locale = get_user_meta($user->id, 'locale', true);

    //message start
    $new_message = "";

    if ($locale == "en_US") {

        $link = get_site_url() . "/" . "en/my-account/";
        $new_message .= 'Welcome' . " " . $username;
        $new_message .= ",";
        $new_message .= "<br>";
        $new_message .= "your account has been approved. Click on the link below to log in";
        //links adding to mail.
        $new_message .= "<br>";
        $new_message .= "<a href='" . $link . "'>Login</a> ";
        $new_message .= "<br>";
        $new_message .= "Best regards" . ",";
        $new_message .= "<br>";
        $new_message .= "Arturo Facchini's team";

    } else {
        //links
        $link = get_site_url() . "/" . "mio-account/";
        $new_message .= 'Benvenuto' . " " . $username;
        $new_message .= ",";
        $new_message .= "<br>";
        $new_message .= "il tuo account è stato approvato. Clicca sul link di seguito per fare il login";
        //links adding to mail.
        $new_message .= "<br>";
        $new_message .= "<a href='" . $link . "'>Login</a> ";
        $new_message .= "<br>";
        $new_message .= "Cordiali saluti" . ",";
        $new_message .= "<br>";
        $new_message .= "Il team di Arturo Facchini";

    }

    return $new_message;

}, 10, 2);

// REGISTRAZIONE - new user deny mail message
add_filter('new_user_approve_deny_user_message', function ($message, $user) {

    add_filter('wp_mail_content_type', function ($content_type) {
        $content_type = 'text/html';
        return $content_type;
    }
    );
    $username = $user->data->user_login;

    $locale = get_user_meta($user->id, 'locale', true);

    //message start
    $new_message = "";

    if ($locale == "en_US") {

        $username = $user->data->user_login;
        $new_message .= "Hello " . $username;
        $new_message .= ",";
        $new_message .= "<br>";
        $new_message .= "Your account has not been approved or has been blocked by the site administrator.";
        $new_message .= "<br>";
        $new_message .= "<br>";
        $new_message .= "Sincerely,";
        $new_message .= "<br>";
        $new_message .= "Arturo Facchini's team";

    } else {

        $username = $user->data->user_login;
        $new_message .= "Salve " . $username;
        $new_message .= ",";
        $new_message .= "<br>";
        $new_message .= "il tuo account non è stato approvato o è stato bloccato dall'amministratore del sito. ";
        $new_message .= "<br>";
        $new_message .= "<br>";
        $new_message .= "Cordiali saluti,";
        $new_message .= "<br>";
        $new_message .= "Il team di Arturo Facchini";

    }

    return $new_message;

}, 10, 2);

//REGISTRAZIONE - dopo registrazione aggiornare meta woocommerce dell'utente
add_action('wpcf7_mail_sent', 'update_user_info', 20, 3);
function update_user_info()
{

    $form = WPCF7_Submission::get_instance();

    $company_name = $form->get_posted_data('company-name');
    $company_address = $form->get_posted_data('company-address');
    $company_phone = $form->get_posted_data('company-phone');
    $vat_number = $form->get_posted_data('vat-number');
    $email = $form->get_posted_data('email');
    $country = $form->get_posted_data('country');
    $language = $form->get_posted_data('language');

    $country_code = array("Afghanistan" => "AF", "Aland Islands" => "AX", "Albania" => "AL", "Algeria" => "DZ", "American Samoa" => "AS", "Andorra" => "AD", "Angola" => "AO", "Anguilla" => "AI", "Antarctica" => "AQ", "Antigua and Barbuda" => "AG", "Argentina" => "AR", "Armenia" => "AM", "Aruba" => "AW", "Australia" => "AU", "Austria" => "AT", "Azerbaijan" => "AZ", "Bahamas" => "BS", "Bahrain" => "BH", "Bangladesh" => "BD", "Barbados" => "BB", "Belarus" => "BY", "Belgium" => "BE", "Belize" => "BZ", "Benin" => "BJ", "Bermuda" => "BM", "Bhutan" => "BT", "Bolivia" => "BO", "Bonaire, Sint Eustatius and Saba" => "BQ", "Bosnia and Herzegovina" => "BA", "Botswana" => "BW", "Bouvet Island" => "BV", "Brazil" => "BR", "British Indian Ocean Territory" => "IO", "Brunei Darussalam" => "BN", "Bulgaria" => "BG", "Burkina Faso" => "BF", "Burundi" => "BI", "Cambodia" => "KH", "Cameroon" => "CM", "Canada" => "CA", "Cape Verde" => "CV", "Cayman Islands" => "KY", "Central African Republic" => "CF", "Chad" => "TD", "Chile" => "CL", "China" => "CN", "Christmas Island" => "CX", "Cocos (Keeling) Islands" => "CC", "Colombia" => "CO", "Comoros" => "KM", "Congo" => "CG", "Congo, Democratic Republic of the Congo" => "CD", "Cook Islands" => "CK", "Costa Rica" => "CR", "Cote D'Ivoire" => "CI", "Croatia" => "HR", "Cuba" => "CU", "Curacao" => "CW", "Cyprus" => "CY", "Czech Republic" => "CZ", "Denmark" => "DK", "Djibouti" => "DJ", "Dominica" => "DM", "Dominican Republic" => "DO", "Ecuador" => "EC", "Egypt" => "EG", "El Salvador" => "SV", "Equatorial Guinea" => "GQ", "Eritrea" => "ER", "Estonia" => "EE", "Ethiopia" => "ET", "Falkland Islands (Malvinas)" => "FK", "Faroe Islands" => "FO", "Fiji" => "FJ", "Finland" => "FI", "France" => "FR", "French Guiana" => "GF", "French Polynesia" => "PF", "French Southern Territories" => "TF", "Gabon" => "GA", "Gambia" => "GM", "Georgia" => "GE", "Germany" => "DE", "Ghana" => "GH", "Gibraltar" => "GI", "Greece" => "GR", "Greenland" => "GL", "Grenada" => "GD", "Guadeloupe" => "GP", "Guam" => "GU", "Guatemala" => "GT", "Guernsey" => "GG", "Guinea" => "GN", "Guinea-Bissau" => "GW", "Guyana" => "GY", "Haiti" => "HT", "Heard Island and Mcdonald Islands" => "HM", "Holy See (Vatican City State)" => "VA", "Honduras" => "HN", "Hong Kong" => "HK", "Hungary" => "HU", "Iceland" => "IS", "India" => "IN", "Indonesia" => "ID", "Iran, Islamic Republic of" => "IR", "Iraq" => "IQ", "Ireland" => "IE", "Isle of Man" => "IM", "Israel" => "IL", "Italy" => "IT", "Jamaica" => "JM", "Japan" => "JP", "Jersey" => "JE", "Jordan" => "JO", "Kazakhstan" => "KZ", "Kenya" => "KE", "Kiribati" => "KI", "Korea, Democratic People's Republic of" => "KP", "Korea, Republic of" => "KR", "Kosovo" => "XK", "Kuwait" => "KW", "Kyrgyzstan" => "KG", "Lao People's Democratic Republic" => "LA", "Latvia" => "LV", "Lebanon" => "LB", "Lesotho" => "LS", "Liberia" => "LR", "Libyan Arab Jamahiriya" => "LY", "Liechtenstein" => "LI", "Lithuania" => "LT", "Luxembourg" => "LU", "Macao" => "MO", "Macedonia, the Former Yugoslav Republic of" => "MK", "Madagascar" => "MG", "Malawi" => "MW", "Malaysia" => "MY", "Maldives" => "MV", "Mali" => "ML", "Malta" => "MT", "Marshall Islands" => "MH", "Martinique" => "MQ", "Mauritania" => "MR", "Mauritius" => "MU", "Mayotte" => "YT", "Mexico" => "MX", "Micronesia, Federated States of" => "FM", "Moldova, Republic of" => "MD", "Monaco" => "MC", "Mongolia" => "MN", "Montenegro" => "ME", "Montserrat" => "MS", "Morocco" => "MA", "Mozambique" => "MZ", "Myanmar" => "MM", "Namibia" => "NA", "Nauru" => "NR", "Nepal" => "NP", "Netherlands" => "NL", "Netherlands Antilles" => "AN", "New Caledonia" => "NC", "New Zealand" => "NZ", "Nicaragua" => "NI", "Niger" => "NE", "Nigeria" => "NG", "Niue" => "NU", "Norfolk Island" => "NF", "Northern Mariana Islands" => "MP", "Norway" => "NO", "Oman" => "OM", "Pakistan" => "PK", "Palau" => "PW", "Palestinian Territory, Occupied" => "PS", "Panama" => "PA", "Papua New Guinea" => "PG", "Paraguay" => "PY", "Peru" => "PE", "Philippines" => "PH", "Pitcairn" => "PN", "Poland" => "PL", "Portugal" => "PT", "Puerto Rico" => "PR", "Qatar" => "QA", "Reunion" => "RE", "Romania" => "RO", "Russian Federation" => "RU", "Rwanda" => "RW", "Saint Barthelemy" => "BL", "Saint Helena" => "SH", "Saint Kitts and Nevis" => "KN", "Saint Lucia" => "LC", "Saint Martin" => "MF", "Saint Pierre and Miquelon" => "PM", "Saint Vincent and the Grenadines" => "VC", "Samoa" => "WS", "San Marino" => "SM", "Sao Tome and Principe" => "ST", "Saudi Arabia" => "SA", "Senegal" => "SN", "Serbia" => "RS", "Serbia and Montenegro" => "CS", "Seychelles" => "SC", "Sierra Leone" => "SL", "Singapore" => "SG", "Sint Maarten" => "SX", "Slovakia" => "SK", "Slovenia" => "SI", "Solomon Islands" => "SB", "Somalia" => "SO", "South Africa" => "ZA", "South Georgia and the South Sandwich Islands" => "GS", "South Sudan" => "SS", "Spain" => "ES", "Sri Lanka" => "LK", "Sudan" => "SD", "Suriname" => "SR", "Svalbard and Jan Mayen" => "SJ", "Swaziland" => "SZ", "Sweden" => "SE", "Switzerland" => "CH", "Syrian Arab Republic" => "SY", "Taiwan, Province of China" => "TW", "Tajikistan" => "TJ", "Tanzania, United Republic of" => "TZ", "Thailand" => "TH", "Timor-Leste" => "TL", "Togo" => "TG", "Tokelau" => "TK", "Tonga" => "TO", "Trinidad and Tobago" => "TT", "Tunisia" => "TN", "Turkey" => "TR", "Turkmenistan" => "TM", "Turks and Caicos Islands" => "TC", "Tuvalu" => "TV", "Uganda" => "UG", "Ukraine" => "UA", "United Arab Emirates" => "AE", "United Kingdom" => "GB", "United States" => "US", "United States Minor Outlying Islands" => "UM", "Uruguay" => "UY", "Uzbekistan" => "UZ", "Vanuatu" => "VU", "Venezuela" => "VE", "Viet Nam" => "VN", "Virgin Islands, British" => "VG", "Virgin Islands, U.s." => "VI", "Wallis and Futuna" => "WF", "Western Sahara" => "EH", "Yemen" => "YE", "Zambia" => "ZM", "Zimbabwe" => "ZW");

    $user = get_user_by('email', $email);
    update_user_meta($user->id, 'vat_number', $vat_number);
    update_user_meta($user->id, 'billing_company', $company_name);
    update_user_meta($user->id, 'billing_country', $country_code[$country[0]]);
    update_user_meta($user->id, 'billing_address_1', $company_address);
    update_user_meta($user->id, 'billing_phone', $company_phone);

    if ($language != "it_IT") {
        update_user_meta($user->id, 'locale', 'en_US');
        update_user_meta($user->id, 'icl_admin_language', 'en');
    } else {
        update_user_meta($user->id, 'locale', $language);
        update_user_meta($user->id, 'icl_admin_language', 'it');
    }
}

// Frontend media library

add_action('wp_enqueue_scripts', 'media_library_enqueue_scripts');
add_filter('ajax_query_attachments_args', 'media_library_filter_media');
//add_shortcode( 'media_library_front_upload', 'media_library_front_upload' );

/**
 * Call wp_enqueue_media() to load up all the scripts we need for media uploader
 */
function media_library_enqueue_scripts()
{
    wp_enqueue_media();
    wp_enqueue_script(
        'media-uploader',
        '/wp-content/themes/af-theme/js/media-uploader.js',
        array('jquery'),
        null
    );
}
/**
 * This filter insures users only see their own media
 */
function media_library_filter_media($query)
{
    // admins get to see everything
    if (!current_user_can('manage_options'))
        $query['author'] = get_current_user_id();
    return $query;
}
function media_library_front_upload($args)
{
    // check if user can upload files
    if (current_user_can('upload_files')) {
        $str = __('Select File', 'af-theme');
        return '<input id="frontend-button" type="file" value="' . $str . '" class="button" style="position: relative; z-index: 1;"><img id="frontend-image" />';
    }
    return __('Please Login To Upload', 'af-theme');
}

// ACCOUNT [account_hero]
function account_hero()
{

    $hero = '';

    if (is_user_logged_in()) {
        $title = '<h1 class="uk-text-center uk-heading-large">' . __('Benvenuto', 'af-theme') . ', ' . display_current_user_display_name() . '</h1>';
        $logout_link = '<p class="uk-text-center">' . add_loginout_link() . '</p>';
        $hero .= $title . $logout_link;
    } else {

        $hero = '<h1 class="uk-text-center uk-heading-large">' . __('Accedi', 'af-theme') . '</h1>';
    }

    return $hero;

}

add_shortcode('account_hero', 'account_hero');

// ACCOUNT [current_user_display_name]
function display_current_user_display_name()
{
    $user = wp_get_current_user();
    $display_name = $user->display_name;
    return $user->display_name;
}
add_shortcode('current_user_display_name', 'display_current_user_display_name');

// ACCOUNT [add_loginout_link]
function add_loginout_link()
{
    if (is_user_logged_in()) {
        $item = '<a class="loginout-link el-link uk-button-text" href="' . wp_logout_url(get_permalink(wc_get_page_id('myaccount'))) . '">' . __('Esci', 'af-theme') . ' <span uk-icon="sign-out"></span></a>';
    }

    return $item;
}
add_shortcode('add_loginout_link', 'add_loginout_link');

// ACCOUNT

function wc_get_custom_account_menu_items()
{
    $endpoints = array(
        'orders' => get_option('woocommerce_myaccount_orders_endpoint', 'orders'),
        'edit-address' => get_option('woocommerce_myaccount_edit_address_endpoint', 'edit-address'),
        'edit-account' => get_option('woocommerce_myaccount_edit_account_endpoint', 'edit-account'),
    );

    $items = array(
        'orders' => __('Orders', 'woocommerce'),
        'edit-address' => _n('Addresses', 'Address', (int) wc_shipping_enabled(), 'woocommerce'),
        'edit-account' => __('Account details', 'woocommerce'),
    );

    // Remove missing endpoints.
    foreach ($endpoints as $endpoint_id => $endpoint) {
        if (empty($endpoint)) {
            unset($items[$endpoint_id]);
        }
    }

    return apply_filters('woocommerce_account_menu_items', $items, $endpoints);
}


function custom_cart_script() {
    ?>
    <script type="text/javascript">
    jQuery(document).ready(function($) {
		var lang = $('html').attr('lang');
		if (lang == 'it-IT'){
			console.log("Italian")		
		} else {
			$('.vpc-cart-component:contains("Colore per l\'interno:")').text('Internal color:');
			$('.vpc-cart-component:contains("Colore per l\'esterno:")').text('External 	color:');
		}
		
		var url = window.location.href;
		  if (url.endsWith("cart") || url.endsWith("cart/") || url.endsWith("carrello") || url.endsWith("carrello/")) {
			
			// Remove minicart inside the cart
			$(document).ready(function() {
			  setTimeout(function() {
				var anchor = $("a[href='#tm-dialog']");
				anchor.remove();
			  }, 1000);
			});
			
			// Avoid the empty cart page by checking if the cart is empty every second
			var element = document.getElementById("page#0");
			var interval = setInterval(function() {
				if (element.innerHTML === "") {
					window.location.reload();
				}
			}, 1000);
		}
    });
    </script>
    <?php
}
add_action('wp_footer', 'custom_cart_script');

?>