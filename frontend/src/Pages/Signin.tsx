import React, { useContext, useState } from 'react'
import { useHistory } from 'react-router-dom'
import Button from '../Components/Button'
import FluidInput from '../Components/FluidInput'
import AppContext from '../Contexts/AppContext'
import './Signin.scss'

function Signin() {
  const appContext = useContext(AppContext)
  const [password, setPassword] = useState<string>('')
  const [username, setUsername] = useState<string>('')
  const [loginError, setLoginError] = useState<boolean>(false)
  const history = useHistory()
  if (appContext?.isLoggedIn) {
    history.replace('/')
  }
  
  async function onLogin() {
    if (appContext) {
      const response = await appContext.backend.login(username, password)
      if (response.success) {
        setLoginError(false)
        appContext.setLoggedIn(true)
        appContext.setCurrUser(response.username)
        history.push('/')
        return
      }
    }
    setLoginError(true)
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="title">
        Login
        </div>
        <FluidInput type="text" label="username" id="username" value={username} setValue={setUsername}/>
        <FluidInput type="password" label="password" id="password" value={password} setValue={setPassword} />
        {
          loginError &&
          <div>Error: Unable to Log In</div>
        }
        <Button onClick={() => onLogin()} buttonClass="login-button">Login</Button>
      </div>
    </div>
  )
}

export default Signin
