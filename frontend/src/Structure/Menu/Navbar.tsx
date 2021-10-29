import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import Button from '../../Components/Button'
import AppContext from '../../Contexts/AppContext'
import Burger from './Burger'
import './Navbar.scss'

export default function Navbar() {
  const [open, setOpen] = useState<boolean>(false)
  const appContext = useContext(AppContext)

  function handleSignOut() {
    appContext?.setCurrUser('')
    appContext?.setLoggedIn(false)
  }

  return (
    <>
      <div className="nav">
        <Link to='/'><p className="navbarLogo" >Game Score Repo</p></Link>
        <div className="menuGroup">
          <Link to='/games'><div className="menuItem">Games</div></Link>
          {
            appContext?.isLoggedIn &&
            <Link to={'/user/' + appContext.currUser}><div className="menuItem">My Account</div></Link>
          }
          {
            appContext?.isLoggedIn &&
            <Link to='/signin'><div className="menuItem" onClick={handleSignOut}>Logout</div></Link>
          }
          {
            !appContext?.isLoggedIn &&
            <Link to='/signin'><div className="menuItem">Login</div></Link>
          }
          {
            !appContext?.isLoggedIn &&
            <Link to='/signup'><Button buttonClass="menuItem signupButton" onClick={()=>{}}>Sign Up</Button></Link>
          }
          <Burger open={open} setOpen={setOpen} handleSignOut={handleSignOut} />
        </div>
      </div>
    </>
  )
}