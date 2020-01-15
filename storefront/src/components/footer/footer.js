/*
 *
 *   Footer component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";

class Footer extends React.Component {
	render() {
		return (
			<div className="footer">
				<div className="container w-container">
					<p className="paragraph">
						© 2018 Bausch &amp; Lomb Incorporated. | EVT.0016.USA.18 | WBTC v1.3.4
						B10enVista Toric Calculator approved for use in the U.S.
					</p>
				</div>
			</div>
		);
	}
}

export default Footer;
