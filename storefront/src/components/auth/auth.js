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
		return g_session_token
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
	 * method login(username, password) get parameters from backend
	 * end put it to local storage
	 */
	async login(username, password) {
		let result = await this.postLoginData(username, password);
		localStorage.setItem("auth", await result.text())
	}

	/*
	 * method postLoginData(username, password) get parameters
	 * and post to backend
	 */
	async postLoginData(username, password) {
		try {
			const url = process.env.REACT_APP_LOGIN;
			const resp = fetch(url, {
				method: "post",
				headers: {
					"Content-type": "application/json; charset=UTF-8"
				},
				body: JSON.stringify({username: username, password: password})
			});
			console.log(resp);
			return resp
		} catch (err) {
			console.log(err)
		}
	}
}
