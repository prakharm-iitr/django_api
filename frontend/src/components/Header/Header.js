import React from 'react';

function Header(props) {

    var title = 'Welcome'
    return(
        <nav className="navbar navbar-dark bg-dark">
            <div className="row col-12 d-flex justify-content-center text-white">
                <span className="h3">{props.title || title}</span>
            </div>
        </nav>
    )
}
export default Header;