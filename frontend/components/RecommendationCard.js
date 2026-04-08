import { useState } from 'react'
import axios from 'axios'

export default function RecommendationCard({ item, onRate, onSave }) {
  const [rating, setRating] = useState(0)

  const handleRate = async () => {
    try {
      const token = (await supabase.auth.getSession()).data.session?.access_token
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/interactions`,
        { item_id: item.id, rating },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      onRate?.(item.id, rating)
      alert('Rating saved!')
    } catch (error) {
      console.error('Error rating item:', error)
    }
  }

  const handleSave = async () => {
    try {
      const token = (await supabase.auth.getSession()).data.session?.access_token
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/saved/${item.id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      onSave?.(item.id)
      alert('Item saved!')
    } catch (error) {
      console.error('Error saving item:', error)
    }
  }

  return (
    <div className="border rounded-lg p-4 shadow-md hover:shadow-lg transition">
      <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
      <p className="text-gray-600 mb-2">{item.description}</p>
      <p className="text-sm text-gray-500 mb-3">Category: {item.category}</p>
      
      <div className="flex space-x-2">
        <select
          value={rating}
          onChange={(e) => setRating(parseInt(e.target.value))}
          className="border rounded px-2 py-1"
        >
          <option value={0}>Rate</option>
          <option value={1}>1⭐</option>
          <option value={2}>2⭐</option>
          <option value={3}>3⭐</option>
          <option value={4}>4⭐</option>
          <option value={5}>5⭐</option>
        </select>
        <button
          onClick={handleRate}
          className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
        >
          Rate
        </button>
        <button
          onClick={handleSave}
          className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
        >
          Save
        </button>
      </div>
    </div>
  )
}
