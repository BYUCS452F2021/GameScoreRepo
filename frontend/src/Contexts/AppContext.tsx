import React from "react"

type backendType = {
  login: Function
  signup: Function
  getGames: Function
  submitScore: Function
  getGame: Function
  getScores: Function
  getUserScores: Function
  getUser: Function
}

export interface AppContextInterface {
  backend: backendType
  currUser: string
  setCurrUser: Function
  isLoggedIn: boolean
  setLoggedIn: Function
}

export const AppContext = React.createContext<AppContextInterface | null>(null)

export default AppContext