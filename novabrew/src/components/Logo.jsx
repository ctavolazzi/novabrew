import logo from '../assets/novabrew-logo.png'

function Logo() {
  return (
    <div className="logo-container">
      <div className="logo-box">
        <img src={logo} alt="NovaBrew Logo" className="logo" />
      </div>
    </div>
  )
}

export default Logo