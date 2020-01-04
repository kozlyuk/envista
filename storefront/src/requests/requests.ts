class Ajax {
	// requestUrl: string;
	constructor() {
		// this.requestUrl = url;
	}
	get(url: string) {
		return new Promise(function(resolve, reject) {
			const xhr = new XMLHttpRequest();
			xhr.open("GET", url, true);
			xhr.onload = function() {
				if (this.status === 200 || this.status === 201) {
					resolve(this.response);
				} else {
					const error = new Error(this.statusText);
					//   error.code = this.status;
					reject(error);
				}
			};
			xhr.onerror = function() {
				reject(new Error("Network Error"));
			};
			xhr.send();
		});
	}
	post(params: any, csrf: string, url: string) {
		return new Promise(function(resolve, reject) {
			const xhr = new XMLHttpRequest();
			// xhr.responseType = "json";
			xhr.open("POST", url, true);
			xhr.setRequestHeader("X-CSRFToken", csrf);
			xhr.setRequestHeader(
				"Content-Type",
				"application/json; charset=utf-8"
			);
			// xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			xhr.onload = function() {
				if (this.status === 200) {
					resolve(this.response);
				} else {
					const error = new Error(this.statusText);
					//   error.code = this.status;
					reject(error);
				}
			};
			xhr.onerror = function() {
				reject(new Error("Network Error"));
			};
			xhr.send(params);
		});
	}
	put(url: string, params: any, csrf: string) {
		return new Promise(function(resolve, reject) {
			const xhr = new XMLHttpRequest();
			xhr.open("PUT", url, true);
			xhr.setRequestHeader("X-CSRFToken", csrf);
			xhr.setRequestHeader(
				"Content-Type",
				"application/json; charset=utf-8"
			);
			xhr.onload = function() {
				if (this.status === 200) {
					resolve(this.response);
				} else {
					const error = new Error(this.statusText);
					//   error.code = this.status;
					reject(error);
				}
			};
			xhr.onerror = function() {
				reject(new Error("Network Error"));
			};
			xhr.send(params);
		});
	}
}

class Cookie {
	args: string;
	constructor(args: string) {
		this.args = args;
	}
	get(name: string) {
		let matches = document.cookie.match(
			new RegExp(
				"(?:^|; )" +
					name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
					"=([^;]*)"
			)
		);
		return matches ? decodeURIComponent(matches[1]) : undefined;
	}
}

function nullCheck(input: any) {
	if (input) {
		return input;
	} else {
		return "";
	}
}

export { Ajax, Cookie, nullCheck };
