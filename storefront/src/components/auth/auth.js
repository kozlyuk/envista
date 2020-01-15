/*
 *
 *   Authenticate module.
 *  
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *  
 *
 */

export default class Auth {
	constructor() {
	}

	/*
	 * isAuthenticate() check if client is authorised
	 * return "true" when user have auth token, and "false" when don't have
	 */
	isAuthenticate() {
		let g_auth = localStorage.getItem("auth");
		if (g_auth == null) {
			g_auth = sessionStorage.getItem("auth");
		}
		return !!g_auth;
	}

	/*
	 * getAuthToken() return auth token from
	 * local storage (in case when user activate checkbox "remember me")
	 * or from session storage
	 */
	getAuthToken() {
		let g_session_token = localStorage.getItem("auth");
		if (g_session_token == null) {
			g_session_token = sessionStorage.getItem("auth");
		}
		return g_session_token.split(':')[1].replace(/["}]+/g, '')
	}

	/*
	 * getCSRFToken() return csrf token
	 */
	static getCSRFToken() {
		return localStorage.getItem("csrf-middleware-token")
	}

	/*
	 * method registration() does registration a new user
	 */
	registration() {

	}

	/*
	 * method login(email, password) get parameters from backend
	 * end put it to local storage
	 */
	async login(email, password) {
		let result = await this.postLoginData(email, password);
		localStorage.setItem("auth", await result.text())
	}

	/*
	 * method postLoginData(email, password) get parameters
	 * and post to backend
	 */
	async postLoginData(email, password) {
		try {
			const url = process.env.REACT_APP_LOGIN;
			const resp = fetch(url, {
				method: "POST",
				headers: {
					"Content-type": "application/json; charset=UTF-8"
				},
				body: JSON.stringify({email: email, password: password})
			});
			console.log(resp);
			return resp
		} catch (err) {
			console.log(err)
		}
	}
}