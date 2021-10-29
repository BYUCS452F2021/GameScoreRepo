import React from 'react'
import ScoreList from '../Components/ScoreList'

type Props = {
  match: any
}

function User(props: Props) {
  return (
    <div className="User">
      <header className="User-header">
        <h1>{'Welcome ' + props.match.params.username}</h1>
        <ScoreList userId={props.match.params.username}/>
      </header>
    </div>
  )
}

export default User
