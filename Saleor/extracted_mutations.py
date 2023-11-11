# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/checkout/graphql/checkout.graphql
CHECKOUTLINESUPDATE_MUTATION = """mutation checkoutLinesUpdate(
	$checkoutId: ID!
	$lines: [CheckoutLineUpdateInput!]!
	$languageCode: LanguageCodeEnum!
) {
	checkoutLinesUpdate(id: $checkoutId, lines: $lines) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTLINEDELETE_MUTATION = """mutation checkoutLineDelete($checkoutId: ID!, $lineId: ID, $languageCode: LanguageCodeEnum!) {
	checkoutLineDelete(id: $checkoutId, lineId: $lineId) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTEMAILUPDATE_MUTATION = """mutation checkoutEmailUpdate($email: String!, $checkoutId: ID!, $languageCode: LanguageCodeEnum!) {
	checkoutEmailUpdate(email: $email, id: $checkoutId) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTCUSTOMERATTACH_MUTATION = """mutation checkoutCustomerAttach($checkoutId: ID!, $languageCode: LanguageCodeEnum!) {
	checkoutCustomerAttach(id: $checkoutId) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTSHIPPINGADDRESSUPDATE_MUTATION = """mutation checkoutShippingAddressUpdate(
	$checkoutId: ID!
	$shippingAddress: AddressInput!
	$validationRules: CheckoutAddressValidationRules
	$languageCode: LanguageCodeEnum!
) {
	checkoutShippingAddressUpdate(
		id: $checkoutId
		shippingAddress: $shippingAddress
		validationRules: $validationRules
	) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTBILLINGADDRESSUPDATE_MUTATION = """mutation checkoutBillingAddressUpdate(
	$checkoutId: ID!
	$billingAddress: AddressInput!
	$validationRules: CheckoutAddressValidationRules
	$languageCode: LanguageCodeEnum!
) {
	checkoutBillingAddressUpdate(
		id: $checkoutId
		billingAddress: $billingAddress
		validationRules: $validationRules
	) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTDELIVERYMETHODUPDATE_MUTATION = """mutation checkoutDeliveryMethodUpdate(
	$checkoutId: ID!
	$deliveryMethodId: ID!
	$languageCode: LanguageCodeEnum!
) {
	checkoutDeliveryMethodUpdate(id: $checkoutId, deliveryMethodId: $deliveryMethodId) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTADDPROMOCODE_MUTATION = """mutation checkoutAddPromoCode($checkoutId: ID, $promoCode: String!, $languageCode: LanguageCodeEnum!) {
	checkoutAddPromoCode(checkoutId: $checkoutId, promoCode: $promoCode) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTREMOVEPROMOCODE_MUTATION = """mutation checkoutRemovePromoCode(
	$checkoutId: ID
	$promoCode: String
	$promoCodeId: ID
	$languageCode: LanguageCodeEnum!
) {
	checkoutRemovePromoCode(checkoutId: $checkoutId, promoCode: $promoCode, promoCodeId: $promoCodeId) {
		errors {
			...CheckoutErrorFragment
		}"""

CHECKOUTCOMPLETE_MUTATION = """mutation checkoutComplete($checkoutId: ID!) {
	checkoutComplete(id: $checkoutId) {
		errors {
			...CheckoutErrorFragment
		}"""

# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/checkout/graphql/payment.graphql
PAYMENTGATEWAYSINITIALIZE_MUTATION = """mutation paymentGatewaysInitialize($checkoutId: ID!, $paymentGateways: [PaymentGatewayToInitialize!]) {
	paymentGatewayInitialize(id: $checkoutId, paymentGateways: $paymentGateways) {
		errors {
			field
			message
			code
		}"""

TRANSACTIONINITIALIZE_MUTATION = """mutation transactionInitialize(
	$checkoutId: ID!
	$action: TransactionFlowStrategyEnum
	$paymentGateway: PaymentGatewayToInitialize!
	$amount: PositiveDecimal
) {
	transactionInitialize(id: $checkoutId, action: $action, paymentGateway: $paymentGateway, amount: $amount) {
		transaction {
			id
			actions
		}"""

TRANSACTIONPROCESS_MUTATION = """mutation transactionProcess($id: ID!, $data: JSON) {
	transactionProcess(id: $id, data: $data) {
		transaction {
			id
			actions
		}"""

# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/checkout/graphql/user.graphql
USERREGISTER_MUTATION = """mutation userRegister($input: AccountRegisterInput!) {
	accountRegister(input: $input) {
		errors {
			message
			field
			code
		}"""

REQUESTPASSWORDRESET_MUTATION = """mutation requestPasswordReset($email: String!, $channel: String!, $redirectUrl: String!) {
	requestPasswordReset(email: $email, channel: $channel, redirectUrl: $redirectUrl) {
		errors {
			message
			field
			code
		}"""

USERADDRESSDELETE_MUTATION = """mutation userAddressDelete($id: ID!) {
	accountAddressDelete(id: $id) {
		user {
			...UserFragment
		}"""

USERADDRESSUPDATE_MUTATION = """mutation userAddressUpdate($id: ID!, $address: AddressInput!) {
	accountAddressUpdate(id: $id, input: $address) {
		user {
			...UserFragment
		}"""

USERADDRESSCREATE_MUTATION = """mutation userAddressCreate($address: AddressInput!, $type: AddressTypeEnum) {
	accountAddressCreate(type: $type, input: $address) {
		user {
			...UserFragment
		}"""

# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/graphql/CheckoutAddLine.graphql
CHECKOUTADDLINE_MUTATION = """mutation CheckoutAddLine($id: ID!, $productVariantId: ID!) {
	checkoutLinesAdd(id: $id, lines: [{ quantity: 1, variantId: $productVariantId }"""

# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/graphql/CheckoutDeleteLines.graphql
CHECKOUTDELETELINES_MUTATION = """mutation CheckoutDeleteLines($checkoutId: ID!, $lineIds: [ID!]!) {
	checkoutLinesDelete(id: $checkoutId, linesIds: $lineIds) {
		checkout {
			id
		}"""

# Mutations from /mnt/data/saleorStoreFront-canary/saleorStoreFront-canary/src/checkout/graphql/index.ts
CHECKOUTLINESUPDATE_MUTATION = """mutation checkoutLinesUpdate(
		$checkoutId: ID!
		$lines: [CheckoutLineUpdateInput!]!
		$languageCode: LanguageCodeEnum!
	) {
		checkoutLinesUpdate(id: $checkoutId, lines: $lines) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTLINEDELETE_MUTATION = """mutation checkoutLineDelete($checkoutId: ID!, $lineId: ID, $languageCode: LanguageCodeEnum!) {
		checkoutLineDelete(id: $checkoutId, lineId: $lineId) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTEMAILUPDATE_MUTATION = """mutation checkoutEmailUpdate($email: String!, $checkoutId: ID!, $languageCode: LanguageCodeEnum!) {
		checkoutEmailUpdate(email: $email, id: $checkoutId) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTCUSTOMERATTACH_MUTATION = """mutation checkoutCustomerAttach($checkoutId: ID!, $languageCode: LanguageCodeEnum!) {
		checkoutCustomerAttach(id: $checkoutId) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTSHIPPINGADDRESSUPDATE_MUTATION = """mutation checkoutShippingAddressUpdate(
		$checkoutId: ID!
		$shippingAddress: AddressInput!
		$validationRules: CheckoutAddressValidationRules
		$languageCode: LanguageCodeEnum!
	) {
		checkoutShippingAddressUpdate(
			id: $checkoutId
			shippingAddress: $shippingAddress
			validationRules: $validationRules
		) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTBILLINGADDRESSUPDATE_MUTATION = """mutation checkoutBillingAddressUpdate(
		$checkoutId: ID!
		$billingAddress: AddressInput!
		$validationRules: CheckoutAddressValidationRules
		$languageCode: LanguageCodeEnum!
	) {
		checkoutBillingAddressUpdate(
			id: $checkoutId
			billingAddress: $billingAddress
			validationRules: $validationRules
		) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTDELIVERYMETHODUPDATE_MUTATION = """mutation checkoutDeliveryMethodUpdate(
		$checkoutId: ID!
		$deliveryMethodId: ID!
		$languageCode: LanguageCodeEnum!
	) {
		checkoutDeliveryMethodUpdate(id: $checkoutId, deliveryMethodId: $deliveryMethodId) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTADDPROMOCODE_MUTATION = """mutation checkoutAddPromoCode($checkoutId: ID, $promoCode: String!, $languageCode: LanguageCodeEnum!) {
		checkoutAddPromoCode(checkoutId: $checkoutId, promoCode: $promoCode) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTREMOVEPROMOCODE_MUTATION = """mutation checkoutRemovePromoCode(
		$checkoutId: ID
		$promoCode: String
		$promoCodeId: ID
		$languageCode: LanguageCodeEnum!
	) {
		checkoutRemovePromoCode(checkoutId: $checkoutId, promoCode: $promoCode, promoCodeId: $promoCodeId) {
			errors {
				...CheckoutErrorFragment
			}"""

CHECKOUTCOMPLETE_MUTATION = """mutation checkoutComplete($checkoutId: ID!) {
		checkoutComplete(id: $checkoutId) {
			errors {
				...CheckoutErrorFragment
			}"""

PAYMENTGATEWAYSINITIALIZE_MUTATION = """mutation paymentGatewaysInitialize($checkoutId: ID!, $paymentGateways: [PaymentGatewayToInitialize!]) {
		paymentGatewayInitialize(id: $checkoutId, paymentGateways: $paymentGateways) {
			errors {
				field
				message
				code
			}"""

TRANSACTIONINITIALIZE_MUTATION = """mutation transactionInitialize(
		$checkoutId: ID!
		$action: TransactionFlowStrategyEnum
		$paymentGateway: PaymentGatewayToInitialize!
		$amount: PositiveDecimal
	) {
		transactionInitialize(
			id: $checkoutId
			action: $action
			paymentGateway: $paymentGateway
			amount: $amount
		) {
			transaction {
				id
				actions
			}"""

TRANSACTIONPROCESS_MUTATION = """mutation transactionProcess($id: ID!, $data: JSON) {
		transactionProcess(id: $id, data: $data) {
			transaction {
				id
				actions
			}"""

USERREGISTER_MUTATION = """mutation userRegister($input: AccountRegisterInput!) {
		accountRegister(input: $input) {
			errors {
				message
				field
				code
			}"""

REQUESTPASSWORDRESET_MUTATION = """mutation requestPasswordReset($email: String!, $channel: String!, $redirectUrl: String!) {
		requestPasswordReset(email: $email, channel: $channel, redirectUrl: $redirectUrl) {
			errors {
				message
				field
				code
			}"""

USERADDRESSDELETE_MUTATION = """mutation userAddressDelete($id: ID!) {
		accountAddressDelete(id: $id) {
			user {
				...UserFragment
			}"""

USERADDRESSUPDATE_MUTATION = """mutation userAddressUpdate($id: ID!, $address: AddressInput!) {
		accountAddressUpdate(id: $id, input: $address) {
			user {
				...UserFragment
			}"""

USERADDRESSCREATE_MUTATION = """mutation userAddressCreate($address: AddressInput!, $type: AddressTypeEnum) {
		accountAddressCreate(type: $type, input: $address) {
			user {
				...UserFragment
			}"""

