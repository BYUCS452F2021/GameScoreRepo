import React, { useContext, useEffect, useState } from 'react'
import AppContext from '../Contexts/AppContext'
import './ScoreList.scss'


type ScoreParam = {
  value: string;
  name: string;
}

type GameParam = {
  description: string;
  name: string;
}

type Game = {
  value: any;
  label: any;
  description: any;
  availableParams: Array<GameParam>;
  imageLink: any;
  owner: any;
  publisher: any;
}

type Score =  {
  game: string;
  username: string;
  timestamp: string;
  params: Array<ScoreParam>;
}

type Props = {
  gameName?: string
  userId?: string
}


function ScoreList(props: Props) {
  const [scores, setScores] = useState<Score[]>([])
  const [game, setGame] = useState<Game>()
  const appContext = useContext(AppContext)

  useEffect(() => {
    async function getScores() {
      const scores = props.gameName ? await appContext?.backend.getScores(props.gameName) : await appContext?.backend.getUserScores(props.userId)
      setScores(scores)
    }
    getScores()
  }, [appContext?.backend, props.gameName, props.userId])

  useEffect(() => {
    async function getGame() {
      const game = props.gameName ? await appContext?.backend.getGame(props.gameName) : null
      setGame(game)
    }
    getGame()
  }, [appContext?.backend, props.gameName, props.userId])

  function ScoreItem(score: Score) {
    return (
      <div className='list-item' key={score.username + score.timestamp + score.game}>
        {
          score.params.map((element: ScoreParam) => {
            console.log(element.value)
            return (
              <div className="info-item">
                {element.name + ': ' + (element.value ? element.value : "")}
              </div>
            )
          })
        }
        {
          props.gameName &&
          <div className="info-item">
            {'Username: ' + score.username}
          </div>
        }
        {
          props.userId &&
          <div className="info-item">
            {'Game: ' + score.game}
          </div>
        }
      </div>
    )
  }

  return (
    <div className="score-page">
      <div className="list-container">
        
        {scores.map((score: Score) => ScoreItem(score))}
      </div>
    </div>
  )
}

export default ScoreList
