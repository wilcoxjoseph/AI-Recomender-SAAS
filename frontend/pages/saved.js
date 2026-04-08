import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import { supabase } from '../utils/supabaseClient'

export default function Saved() {
  const [savedItems, setSavedItems] = useState([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    checkUser()
    fetchSavedItems()
  }, [])

  const checkUser = async () => {
    const { data: { session } } = await supabase.auth.getSession()
    if (!session) {
      router.push('/login')
    }
  }

  const fetchSavedItems = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/saved`,
        {
          headers: { Authorization: `Bearer ${session.access_token}` }
        }
      )
      setSavedItems(response.data.saved_items)
    } catch (error) {
      console.error('Error fetching saved items:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Saved Items</h1>
        {savedItems.length === 0 ? (
          <p className="text-gray-500">No saved items yet. Start saving recommendations!</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedItems.map((item) => (
              <div key={item.id} className="border rounded-lg p-4 shadow-md">
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-600 mb-2">{item.description}</p>
                <p className="text-sm text-gray-500">Category: {item.category}</p>
                <p className="text-xs text-gray-400 mt-2">
                  Saved at: {new Date(item.saved_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
