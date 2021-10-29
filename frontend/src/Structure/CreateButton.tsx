
import React, { useContext, useState } from 'react'
import ReactDOM from 'react-dom'
import Button from '../Components/Button'
import ScoreModal from '../Components/ScoreModal'
import AppContext from '../Contexts/AppContext'
import './CreateButton.scss'

function CreateButton() {
  const appContext = useContext(AppContext)
  const [isAddingScore, setAddingScore] = useState<boolean>(false)
  function onClick() {
    setAddingScore(true)
  }
  return ReactDOM.createPortal((
    <>
      {
        isAddingScore &&
        <ScoreModal onClose={() => setAddingScore(false)} />
      }
      {
          appContext?.isLoggedIn &&
          <Button buttonClass="createButton" onClick={onClick}>+</Button>
      }
    </>
  ), document.getElementById('root') || document.createElement('div'))
}

export default CreateButton