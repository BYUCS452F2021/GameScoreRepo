import React, { useContext, useEffect, useState } from 'react'
import AppContext from '../Contexts/AppContext'
import './ScoreList.scss'


type Score = {
  scoreId: number
  gameName: string
  username: string
  value: number
}

type Props = {
  gameId?: string
  userId?: string
}


function ScoreList(props: Props) {
  const [scores, setScores] = useState<Score[]>([])
  const appContext = useContext(AppContext)
  
  useEffect(() => {
    async function getScores() {
      const scores = props.gameId ? await appContext?.backend.getScores(props.gameId) : await appContext?.backend.getUserScores(props.userId)
      setScores(scores)
    }
    getScores()
  }, [appContext?.backend, props.gameId, props.userId])

  function ScoreItem(score: Score) {
    return (
      <div className='list-item' key={score.scoreId}>
        <div className="info-item">
          {'Game: ' + score.gameName}
        </div>
        <div className="info-item">
          {'Username: ' + score.username}
        </div>
        <div className="info-item">
          {'Score: ' + score.value}
        </div>
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
