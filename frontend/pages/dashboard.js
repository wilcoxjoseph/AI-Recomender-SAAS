import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import Navbar from '../components/Navbar'
import RecommendationCard from '../components/RecommendationCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { supabase } from '../utils/supabaseClient'

export default function Dashboard() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    checkUser()
    fetchRecommendations()
  }, [])

  const checkUser = async () => {
    const { data: { session } } = await supabase.auth.getSession()
    if (!session) {
      router.push('/login')
    }
  }

  const fetchRecommendations = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/recommendations`,
        {
          headers: { Authorization: `Bearer ${session.access_token}` }
        }
      )
      setRecommendations(response.data.recommendations)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Your Personalized Recommendations</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendations.map((item) => (
            <RecommendationCard key={item.id} item={item} />
          ))}
        </div>
      </div>
    </div>
  )
}
