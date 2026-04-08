import { useRouter } from 'next/router'
import { supabase } from '../utils/supabaseClient'

export default function Navbar() {
  const router = useRouter()

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
  }

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">AI Recommender</div>
        <div className="space-x-4">
          <button
            onClick={() => router.push('/dashboard')}
            className="hover:text-gray-300"
          >
            Dashboard
          </button>
          <button
            onClick={() => router.push('/saved')}
            className="hover:text-gray-300"
          >
            Saved
          </button>
          <button
            onClick={handleLogout}
            className="bg-red-600 px-4 py-2 rounded hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}
