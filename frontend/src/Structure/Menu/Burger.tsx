import { MouseEventHandler } from 'react'
import './Burger.scss'

import RightNav from './RightNav'

type Props = {
  open: boolean
  setOpen: Function
  handleSignOut: MouseEventHandler<HTMLLIElement>
}

function Burger(props: Props) {
  return (
    <>
      <div className="burger" onClick={() => props.setOpen(!props.open)}>
        <div className="menus"/>
        <div className="menus"/>
        <div className="menus"/>
      </div>
      <RightNav open={props.open} handleSignOut={props.handleSignOut} />
    </>
  )
}
export default Burger