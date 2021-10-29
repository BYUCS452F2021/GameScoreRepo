import React from 'react'
import { Switch, Route } from 'react-router-dom'

import Home from '../Pages/Home'
import Signup from '../Pages/Signup'
import Game from '../Pages/Game'
import Signin from '../Pages/Signin'
import User from '../Pages/User'
import Games from '../Pages/Games'

const Main = () => {
  return (
    <Switch>
      <Route exact path='/' component={Home}></Route>
      <Route exact path='/signup' component={Signup}></Route>
      <Route exact path='/games' component={Games}></Route>
      <Route exact path='/game/:id' component={Game}></Route>
      <Route exact path='/signin' component={Signin}></Route>
      <Route exact path='/user/:username' component={User}></Route>
    </Switch>
  )
}

export default Main