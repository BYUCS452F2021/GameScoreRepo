import axios from "axios"

const BASE_URL = 'http://127.0.0.1:5000'
const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
    "Access-Control-Allow-Origin": "*",
  }
}

const gameMap = {
  1: 'Catan',
  2: 'Ticket To Ride',
  3: 'Carcassone',
  4: 'Terraforming Mars',
  5: '7 Wonders'
}

type RawScore =  [
  number,
  1 | 2 | 3 | 4 | 5,
  number,
  string,
  string
]

type Score = {
  scoreId: number
  gameName: string
  username: string
  value: number
}

function formatScore(score: RawScore)  {
  return {
    scoreId: score[0],
    gameName: gameMap[score[1]],
    username: score[3],
    value: score[2]
  }
}

export const gameScoreBackend = {
  login: async function (username: string, password: string) {
    const data = JSON.stringify({
      username: username,
      password: password,
    })
    const response = await axios.post(BASE_URL + '/login', data, axiosConfig)
    if (response.data.status === 'success') {
      return {
        success: true,
        email: response.data.email,
        username: response.data.username
      }
    }
    return {
      success: false,
      message: 'Unable to log in'
    }
  },
  signup: async function (username: string, password: string, email: string) {
    const data = JSON.stringify({
      username: username,
      password: password,
      email: email,
    })
    const response = await axios.post(BASE_URL + '/register', data, axiosConfig)
    if (response.data.status === 'success') {
      return {
        success: true,
        email: response.data.email,
        username: response.data.username
      }
    }
    return {
      success: false,
      message: 'Unable to sign up'
    }
  },
  getGames: async function () {
    const response = await axios.get(BASE_URL + '/games')
    if (response.status === 200) {
      let result: { value: any; label: any; }[] = []
      response.data.forEach((element: any) => {
        result.push({value: element.game_id, label: element.name})
      })
      return result
    }
    return []
  },
  submitScore: async function(gameId: string, value: number, username: string) {
    const data = JSON.stringify({
      game_id: gameId,
      value: value,
      username: username,
    })
    const response = await axios.post(BASE_URL + '/score', data, axiosConfig)
    if (response.data.status === 'success') {
      return {
        success: true,
        email: response.data.email,
        username: response.data.username
      }
    }
    return {
      success: false,
      message: 'Unable to submit score'
    }
  },
  getGame: async function(gameId: string) {
    const response = await axios.get(BASE_URL + '/game?game_id=' + gameId)
    if (response.status === 200) {
      return response.data[0]
    }
    return {}
  },
  getScores: async function(gameId: string) {
    const response = await axios.get(BASE_URL + '/game_scores?game_id=' + gameId)
    if (response.status === 200) {
      let result: Score[] = []
      response.data.forEach(async (element: RawScore) => {
        result.push(formatScore(element))
      })
      return result
    }
    return []
  },
  getUserScores: async function(username: string) {
    const response = await axios.get(BASE_URL + '/user_scores?username=' + username)
    if (response.status === 200) {
      let result: Score[] = []
      response.data.forEach(async (element: RawScore) => {
        result.push(formatScore(element))
      })
      return result
    }
    return []
  },
  getUser: async function(username: string) {
    const response = await axios.get(BASE_URL + '/user?username=' + username)
    if (response.status === 200) {
      return response.data[0]
    }
    return {}
  },

}

export default gameScoreBackend