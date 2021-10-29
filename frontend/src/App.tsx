import React, { useState } from 'react'
import { AppContextInterface, AppContext } from './Contexts/AppContext'
import Main from './Structure/Main'
import gameScoreBackend from './Backends/gameScoreBackend'
import { BrowserRouter } from 'react-router-dom'
import Navbar from './Structure/Menu/Navbar'
import CreateButton from './Structure/CreateButton'
import './App.scss'



function App() {
  const [isLoggedIn, setLoggedIn] = useState<boolean>(false)
  const [currUser, setCurrUser] = useState<string>('')
  const appData: AppContextInterface = {
    backend: gameScoreBackend,
    currUser: currUser,
    setCurrUser: setCurrUser,
    isLoggedIn: isLoggedIn,
    setLoggedIn: setLoggedIn
  }

  return (
    <div className="App">
      <BrowserRouter>
        <AppContext.Provider value={appData}>
          <Navbar />
          <Main />
          <CreateButton />
        </AppContext.Provider>
      </BrowserRouter>
    </div>
  )
}

export default App
