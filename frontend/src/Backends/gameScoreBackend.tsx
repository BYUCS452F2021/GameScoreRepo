import axios from "axios"

const BASE_URL = 'http://127.0.0.1:5000'
const axiosConfig = {
  headers: {
    'Content-Type': 'application/json',
    "Access-Control-Allow-Origin": "*",
  }
}

type Score =  {
  game: string;
  username: string;
  timestamp: string;
  params: Array<string>;
}

type Param = {
  description: string;
  name: string;
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
    console.log(response)
    if (response.status === 200) {
      let result: {
        value: any;
        label: any;
        description: any;
        availableParams: Array<Param>;
        imageLink: any;
        owner: any;
        publisher: any;
      }[] = []
      response.data.forEach((element: any, index: number) => {
        result.push({
          value: index+1,
          label: element.name,
          description: element.description,
          availableParams: element.available_params,
          imageLink: element.image_link,
          owner: element.username,
          publisher: element.publisher
        })
      })
      return result
    }
    return []
  },
  submitScore: async function(gameId: string, values: [string, number], username: string) {
    const data = JSON.stringify({
      game: gameId,
      values: values,
      username: username,
    })
    const response = await axios.post(BASE_URL + '/score', data, axiosConfig)
    if (response.data.status === 'success') {
      return {
        success: true
      }
    }
    return {
      success: false,
      message: 'Unable to submit score'
    }
  },
  getGame: async function(gameName: string) {
    const response = await axios.get(BASE_URL + '/game?name=' + gameName)
    if (response.status === 200) {
      return response.data
    }
    return {}
  },
  getScores: async function(gameName: string) {
    const response = await axios.get(BASE_URL + '/game_scores?game_name=' + gameName)
    if (response.status === 200) {
      let result: Score[] = []
      response.data.forEach(async (element: Score) => {
        result.push(element)
      })
      return result
    }
    return []
  },
  getUserScores: async function(username: string) {
    const response = await axios.get(BASE_URL + '/user_scores?username=' + username)
    if (response.status === 200) {
      let result: Score[] = []
      response.data.forEach(async (element: Score) => {
        result.push(element)
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