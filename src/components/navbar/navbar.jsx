import './navbar.css'
const Navbar = () => {
  return (
    <nav className='navbar'>
        <h1 className='logo'>NOTESCOON</h1>
        <ul className='nav-links'>
            <li><a href="#">FAVORITES</a></li>
            <li><a href="#">ALBUMS</a></li>
            <li><a href="#">REMINDERS</a></li>
        </ul>
    </nav>
  )
}

export default Navbar