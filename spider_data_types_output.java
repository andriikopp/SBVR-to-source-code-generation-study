class product {
	private String title;

	public void set_title(String value) throws Exception {
		if (value != null) {
			this.title = value;
		} else {
			throw new Exception("title value is null");
		}
	}

	public String get_title() {
		return this.title;
	}

	private String description;

	public void set_description(String value) {
		this.description = value;
	}

	public String get_description() {
		return this.description;
	}

	private String image;

	public void set_image(String value) {
		this.image = value;
	}

	public String get_image() {
		return this.image;
	}

	private String price;

	public void set_price(String value) throws Exception {
		if (value != null) {
			this.price = value;
		} else {
			throw new Exception("price value is null");
		}
	}

	public String get_price() {
		return this.price;
	}

	private Double amount;

	public void set_amount(Double value) throws Exception {
		if (value != null) {
			this.amount = value;
		} else {
			throw new Exception("amount value is null");
		}
	}

	public Double get_amount() {
		return this.amount;
	}

	private Integer votes;

	public void set_votes(Integer value) {
		this.votes = value;
	}

	public Integer get_votes() {
		return this.votes;
	}

	private String rating;

	public void set_rating(String value) {
		this.rating = value;
	}

	public String get_rating() {
		return this.rating;
	}

	private brand brandObj;

	public void set_brandObj(brand value) throws Exception {
		if (value != null) {
			this.brandObj = value;
		} else {
			throw new Exception("brand value is null");
		}
	}

	public brand get_brandObj() {
		return this.brandObj;
	}

	private category categoryObj;

	public void set_categoryObj(category value) throws Exception {
		if (value != null) {
			this.categoryObj = value;
		} else {
			throw new Exception("category value is null");
		}
	}

	public category get_categoryObj() {
		return this.categoryObj;
	}

}

class category {
	private String title;

	public void set_title(String value) throws Exception {
		if (value != null) {
			this.title = value;
		} else {
			throw new Exception("title value is null");
		}
	}

	public String get_title() {
		return this.title;
	}

	private String description;

	public void set_description(String value) {
		this.description = value;
	}

	public String get_description() {
		return this.description;
	}

	private String image;

	public void set_image(String value) {
		this.image = value;
	}

	public String get_image() {
		return this.image;
	}

}

class brand {
	private String title;

	public void set_title(String value) throws Exception {
		if (value != null) {
			this.title = value;
		} else {
			throw new Exception("title value is null");
		}
	}

	public String get_title() {
		return this.title;
	}

	private String image;

	public void set_image(String value) {
		this.image = value;
	}

	public String get_image() {
		return this.image;
	}

	private String description;

	public void set_description(String value) {
		this.description = value;
	}

	public String get_description() {
		return this.description;
	}

	private String origin_country;

	public void set_origin_country(String value) throws Exception {
		if (value != null) {
			this.origin_country = value;
		} else {
			throw new Exception("origin_country value is null");
		}
	}

	public String get_origin_country() {
		return this.origin_country;
	}

}

