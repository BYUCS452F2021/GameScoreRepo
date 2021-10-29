import React from 'react'
import { MouseEventHandler, useContext } from 'react'
import { Link } from 'react-router-dom'
import Button from '../../Components/Button'
import AppContext from '../../Contexts/AppContext'
import './RightNav.scss'

type Props = {
  open: boolean
  handleSignOut: MouseEventHandler<HTMLLIElement>
}

function RightNav(props: Props) {
  const appContext = useContext(AppContext)
  return (
    <>
      {
        props.open &&
        <ul className="menuList">
          <div className="webName">Game Score Repo</div>
          <Link to='/games'><li className="rightNavItem">Games</li></Link>
          {
            appContext?.isLoggedIn &&
            <Link to={'/user/' + appContext.currUser}><li className="rightNavItem">My Account</li></Link>
          }
          {
            appContext?.isLoggedIn &&
            <Link to='/signin'><li className="rightNavItem" onClick={props.handleSignOut}>Logout</li></Link>
          }
          {
            !appContext?.isLoggedIn &&
            <Link to='/signin'><li className="rightNavItem">Login</li></Link>
          }
          {
            !appContext?.isLoggedIn &&
            <Link to='/signup'><Button buttonClass="rightNavItem signupButton" onClick={()=>{}}>Sign Up</Button></Link>
          }
        </ul>
      }
    </>
  )
}

export default RightNav