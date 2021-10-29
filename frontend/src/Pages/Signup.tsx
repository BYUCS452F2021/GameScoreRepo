import React, { useContext, useState } from 'react'
import { useHistory } from 'react-router-dom'
import Button from '../Components/Button'
import FluidInput from '../Components/FluidInput'
import AppContext from '../Contexts/AppContext'
import './Signup.scss'

function Signup() {
  const appContext = useContext(AppContext)
  const [password, setPassword] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  const [username, setUsername] = useState<string>('')
  const [signupError, setSignupError] = useState<boolean>(false)

  const history = useHistory()
  if (appContext?.isLoggedIn) {
    history.replace('/')
  }

  async function onSignup() {
    if (appContext) {
      const response = await appContext.backend.signup(username, password, email)
      if (response.success) {
        setSignupError(false)
        appContext.setLoggedIn(true)
        appContext.setCurrUser(response.username)
        return
      }
    }
    setSignupError(true)
  }

  return (
    <div className="signup-page">
      <div className="signup-container">
        <div className="title">
        Sign Up
        </div>
        <FluidInput type="text" label="username" id="username" value={username} setValue={setUsername}/>
        <FluidInput type="text" label="email" id="email" value={email} setValue={setEmail}/>
        <FluidInput type="password" label="password" id="password" value={password} setValue={setPassword} />
        {
          signupError &&
          <div>Error: Unable to Sign Up</div>
        }
        <Button onClick={() => onSignup()} buttonClass="signup-button">Sign Up</Button>
      </div>
    </div>
  )
}

export default Signup
