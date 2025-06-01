
// import { useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Card } from "@/components/ui/card";
// import { Textarea } from "@/components/ui/textarea";
// import { Badge } from "@/components/ui/badge";
// import { Separator } from "@/components/ui/separator";
// import { 
//   MapPin, 
//   Calendar, 
//   Users, 
//   Plane, 
//   Mountain, 
//   Camera,
//   Star,
//   Clock,
//   Globe,
//   Send,
//   Sparkles,
//   Heart
// } from "lucide-react";
// import { toast } from "@/hooks/use-toast";

// interface DestinationInfo {
//   destination: string;
//   duration: number;
//   interests: string[];
//   travel_style?: string;
// }

// interface Place {
//   name: string;
//   type: string;
//   rating?: number;
//   description?: string;
// }

// interface TravelResponse {
//   itinerary: string;
//   places: Place[];
//   status: string;
//   destination_info: DestinationInfo;
// }

// const Index = () => {
//   const [message, setMessage] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [response, setResponse] = useState<TravelResponse | null>(null);

//   const handleSubmit = async () => {
//     if (!message.trim()) {
//       toast({
//         title: "נא הזן הודעה",
//         description: "אנא ספר לנו לאן אתה רוצה לנסוע",
//         variant: "destructive"
//       });
//       return;
//     }

//     setLoading(true);
//     try {
//       console.log("Sending request to Python API...");
//       const apiResponse = await fetch("http://localhost:8000/plan-trip", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ message }),
//       });

//       if (!apiResponse.ok) {
//         throw new Error(`HTTP error! status: ${apiResponse.status}`);
//       }

//       const data: TravelResponse = await apiResponse.json();
//       console.log("Received response:", data);
//       setResponse(data);

//       toast({
//         title: "התוכנית מוכנה!",
//         description: "התוכנית שלך נוצרה בהצלחה",
//       });
//     } catch (error) {
//       console.error("Error planning trip:", error);
//       toast({
//         title: "שגיאה",
//         description: "התרחשה שגיאה בתכנון הטיול. אנא נסה שוב.",
//         variant: "destructive"
//       });
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
//       {/* Hero Section */}
//       <div className="relative overflow-hidden travel-gradient">
//         <div className="absolute inset-0 bg-black/20"></div>
//         <div className="relative container mx-auto px-4 py-24 text-center text-white">
//           <div className="floating-animation">
//             <Plane className="w-16 h-16 mx-auto mb-6 text-white/90" />
//           </div>
//           <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fade-in">
//             מתכנן הטיולים שלך
//           </h1>
//           <p className="text-xl md:text-2xl mb-8 text-white/90 animate-fade-in travel-animation-delay-1">
//             בינה מלאכותית מתקדמת לתכנון הטיול המושלם עבורך
//           </p>
//           <div className="flex justify-center space-x-8 text-white/80 animate-fade-in travel-animation-delay-2">
//             <div className="flex items-center space-x-2">
//               <MapPin className="w-5 h-5" />
//               <span>יעדים ברחבי העולם</span>
//             </div>
//             <div className="flex items-center space-x-2">
//               <Calendar className="w-5 h-5" />
//               <span>תכנון מותאם אישית</span>
//             </div>
//             <div className="flex items-center space-x-2">
//               <Sparkles className="w-5 h-5" />
//               <span>המלצות חכמות</span>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-16">
//         {/* Trip Planning Form */}
//         <Card className="max-w-4xl mx-auto p-8 mb-12 travel-card-hover shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
//           <div className="text-center mb-8">
//             <h2 className="text-3xl font-bold travel-text-gradient mb-4">
//               איפה נתחיל את ההרפתקה?
//             </h2>
//             <p className="text-gray-600 text-lg">
//               ספר לנו לאן אתה רוצה לנסוע, כמה זמן יש לך ומה מעניין אותך
//             </p>
//           </div>

//           <div className="space-y-6">
//             <div className="relative">
//               <Textarea
//                 placeholder="לדוגמה: אני רוצה טיול של 5 ימים לפריז עם אוכל ומוזיאונים..."
//                 value={message}
//                 onChange={(e) => setMessage(e.target.value)}
//                 className="min-h-[120px] text-lg border-2 border-purple-200 focus:border-purple-400 transition-colors resize-none"
//                 dir="rtl"
//               />
//               <div className="absolute bottom-4 left-4">
//                 <Globe className="w-5 h-5 text-gray-400" />
//               </div>
//             </div>

//             <Button
//               onClick={handleSubmit}
//               disabled={loading}
//               className="w-full travel-gradient text-white text-lg py-6 rounded-xl hover:scale-105 transition-all duration-300 pulse-glow"
//             >
//               {loading ? (
//                 <div className="flex items-center space-x-2">
//                   <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
//                   <span>מכין את התוכנית שלך...</span>
//                 </div>
//               ) : (
//                 <div className="flex items-center space-x-2">
//                   <Send className="w-5 h-5" />
//                   <span>תכנן לי טיול!</span>
//                 </div>
//               )}
//             </Button>
//           </div>
//         </Card>

//         {/* Results Section */}
//         {response && (
//           <div className="max-w-6xl mx-auto space-y-8 animate-fade-in">
//             {/* Destination Info */}
//             {response.destination_info.destination && (
//               <Card className="p-8 travel-card-hover shadow-xl border-0 bg-white/90 backdrop-blur-sm">
//                 <div className="flex items-center space-x-4 mb-6">
//                   <MapPin className="w-8 h-8 text-purple-600" />
//                   <h3 className="text-2xl font-bold travel-text-gradient">
//                     פרטי הטיול
//                   </h3>
//                 </div>
//                 <div className="grid md:grid-cols-3 gap-6">
//                   <div className="text-center p-4 rounded-xl travel-gradient-light">
//                     <Globe className="w-8 h-8 mx-auto mb-2 text-purple-700" />
//                     <h4 className="font-semibold text-purple-900">יעד</h4>
//                     <p className="text-purple-800">{response.destination_info.destination}</p>
//                   </div>
//                   <div className="text-center p-4 rounded-xl travel-gradient-light">
//                     <Calendar className="w-8 h-8 mx-auto mb-2 text-purple-700" />
//                     <h4 className="font-semibold text-purple-900">משך הטיול</h4>
//                     <p className="text-purple-800">{response.destination_info.duration} ימים</p>
//                   </div>
//                   <div className="text-center p-4 rounded-xl travel-gradient-light">
//                     <Heart className="w-8 h-8 mx-auto mb-2 text-purple-700" />
//                     <h4 className="font-semibold text-purple-900">תחומי עניין</h4>
//                     <div className="flex flex-wrap justify-center gap-2 mt-2">
//                       {response.destination_info.interests.map((interest, index) => (
//                         <Badge key={index} variant="secondary" className="bg-purple-100 text-purple-800">
//                           {interest}
//                         </Badge>
//                       ))}
//                     </div>
//                   </div>
//                 </div>
//               </Card>
//             )}

//             {/* Places */}
//             {response.places && response.places.length > 0 && (
//               <Card className="p-8 travel-card-hover shadow-xl border-0 bg-white/90 backdrop-blur-sm">
//                 <div className="flex items-center space-x-4 mb-6">
//                   <Camera className="w-8 h-8 text-purple-600" />
//                   <h3 className="text-2xl font-bold travel-text-gradient">
//                     מקומות מומלצים לביקור
//                   </h3>
//                 </div>
//                 <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
//                   {response.places.slice(0, 9).map((place, index) => (
//                     <div key={index} className="p-4 rounded-xl border border-purple-200 travel-card-hover bg-gradient-to-br from-white to-purple-50">
//                       <div className="flex items-start justify-between mb-3">
//                         <h4 className="font-semibold text-purple-900 flex-1">{place.name}</h4>
//                         {place.rating && (
//                           <div className="flex items-center space-x-1 text-yellow-500">
//                             <Star className="w-4 h-4 fill-current" />
//                             <span className="text-sm text-gray-700">{place.rating}</span>
//                           </div>
//                         )}
//                       </div>
//                       <Badge variant="outline" className="mb-2 border-purple-300 text-purple-700">
//                         {place.type}
//                       </Badge>
//                       {place.description && (
//                         <p className="text-sm text-gray-600 line-clamp-3">{place.description}</p>
//                       )}
//                     </div>
//                   ))}
//                 </div>
//               </Card>
//             )}

//             {/* Itinerary */}
//             <Card className="p-8 travel-card-hover shadow-xl border-0 bg-white/90 backdrop-blur-sm">
//               <div className="flex items-center space-x-4 mb-6">
//                 <Clock className="w-8 h-8 text-purple-600" />
//                 <h3 className="text-2xl font-bold travel-text-gradient">
//                   תוכנית הטיול המלאה
//                 </h3>
//               </div>
//               <div className="prose prose-lg max-w-none" dir="rtl">
//                 <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl border border-purple-200">
//                   <pre className="whitespace-pre-wrap text-gray-800 font-sans leading-relaxed">
//                     {response.itinerary}
//                   </pre>
//                 </div>
//               </div>
//             </Card>
//           </div>
//         )}

//         {/* Features Section */}
//         {!response && (
//           <div className="max-w-6xl mx-auto">
//             <h2 className="text-3xl font-bold text-center travel-text-gradient mb-12">
//               למה לבחור במתכנן שלנו?
//             </h2>
//             <div className="grid md:grid-cols-3 gap-8">
//               <Card className="p-6 text-center travel-card-hover shadow-xl border-0 bg-white/80 backdrop-blur-sm">
//                 <div className="floating-animation travel-animation-delay-1">
//                   <Mountain className="w-12 h-12 mx-auto mb-4 text-purple-600" />
//                 </div>
//                 <h3 className="text-xl font-semibold mb-3 travel-text-gradient">
//                   בינה מלאכותית מתקדמת
//                 </h3>
//                 <p className="text-gray-600">
//                   אלגוריתמים חכמים שיוצרים תוכניות טיול מותאמות אישית
//                 </p>
//               </Card>

//               <Card className="p-6 text-center travel-card-hover shadow-xl border-0 bg-white/80 backdrop-blur-sm">
//                 <div className="floating-animation travel-animation-delay-2">
//                   <Users className="w-12 h-12 mx-auto mb-4 text-purple-600" />
//                 </div>
//                 <h3 className="text-xl font-semibold mb-3 travel-text-gradient">
//                   מותאם אישית
//                 </h3>
//                 <p className="text-gray-600">
//                   כל תוכנית נבנית במיוחד עבורך בהתאם להעדפות ולתקציב שלך
//                 </p>
//               </Card>

//               <Card className="p-6 text-center travel-card-hover shadow-xl border-0 bg-white/80 backdrop-blur-sm">
//                 <div className="floating-animation travel-animation-delay-3">
//                   <Globe className="w-12 h-12 mx-auto mb-4 text-purple-600" />
//                 </div>
//                 <h3 className="text-xl font-semibold mb-3 travel-text-gradient">
//                   יעדים ברחבי העולם
//                 </h3>
//                 <p className="text-gray-600">
//                   מאגר עצום של יעדים ואטרקציות מכל רחבי העולם
//                 </p>
//               </Card>
//             </div>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Index;
"use client"

import type React from "react"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  MapPin,
  Calendar,
  Heart,
  Plane,
  Search,
  Loader2,
  Star,
  Clock,
  Users,
  Camera,
  Mountain,
  Utensils,
  Building,
  Palette,
  Gamepad2,
  Waves,
  ShoppingBag,
  Music,
  Sparkles,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"

interface TravelResponse {
  itinerary: string
  places: Array<{
    name: string
    type: string
    rating?: number
    description?: string
    address?: string
  }>
  status: string
  destination_info: {
    destination: string
    duration: number
    interests: string[]
    travel_style: string
  }
}

const interestIcons = {
  food: Utensils,
  history: Building,
  nature: Mountain,
  art: Palette,
  technology: Gamepad2,
  adventure: Mountain,
  relaxation: Waves,
  nightlife: Music,
  shopping: ShoppingBag,
  general: Camera,
}

const gradients = [
  "from-purple-400 via-pink-500 to-red-500",
  "from-blue-400 via-purple-500 to-pink-500",
  "from-green-400 via-blue-500 to-purple-600",
  "from-yellow-400 via-orange-500 to-red-500",
  "from-indigo-400 via-purple-500 to-pink-500",
]

export default function Index() {
  const [request, setRequest] = useState("")
  const [response, setResponse] = useState<TravelResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!request.trim()) return

    setLoading(true)
    setError("")
    setResponse(null)

    try {
      const res = await fetch("http://localhost:8001/plan-trip", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: request }),
      })

      if (!res.ok) {
        throw new Error("Failed to plan trip")
      }

      const data: TravelResponse = await res.json()
      setResponse(data)
    } catch (err) {
      setError("Failed to plan your trip. Please try again.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatItinerary = (itinerary: string) => {
    return itinerary.split("\n").map((line, index) => {
      if (line.startsWith("# ")) {
        return (
          <h1 key={index} className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Sparkles className="text-yellow-500" />
            {line.replace("# ", "")}
          </h1>
        )
      }
      if (line.startsWith("## ")) {
        return (
          <h2 key={index} className="text-2xl font-semibold text-gray-700 mt-8 mb-4 flex items-center gap-2">
            <Calendar className="text-blue-500" />
            {line.replace("## ", "")}
          </h2>
        )
      }
      if (line.startsWith("### ")) {
        return (
          <h3 key={index} className="text-xl font-medium text-gray-600 mt-6 mb-3 flex items-center gap-2">
            <Clock className="text-green-500" />
            {line.replace("### ", "")}
          </h3>
        )
      }
      if (line.startsWith("**") && line.endsWith("**")) {
        return (
          <p key={index} className="font-semibold text-gray-800 mt-4 mb-2">
            {line.replace(/\*\*/g, "")}
          </p>
        )
      }
      if (line.startsWith("- ")) {
        return (
          <li key={index} className="text-gray-600 ml-4 mb-1">
            {line.replace("- ", "")}
          </li>
        )
      }
      if (line.trim()) {
        return (
          <p key={index} className="text-gray-600 mb-3 leading-relaxed">
            {line}
          </p>
        )
      }
      return <br key={index} />
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-gray-50 to-gray-50">
      {/* Header */}
      <motion.header
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="bg-white/80 backdrop-blur-md shadow-md border-b border-white/20"
      >
        <div className="container mx-auto px-4 py-2">
          <div className="flex items-center justify-center gap-3">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
            >
              <Plane className="w-8 h-8 text-amber-400" />
            </motion.div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-teal-500 to-amber-400 bg-clip-text text-transparent">
              AI Travel Planner
            </h1>
          </div>
          <p className="text-center text-gray-600 mt-2">Plan your perfect trip with AI-powered recommendations</p>
        </div>
      </motion.header>

      <div className="container mx-auto px-4 py-8">
        {/* Main Form */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <Card className="bg-white/90 backdrop-blur-sm shadow-2xl border-0 overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-teal-400 to-amber-400 text-white">
              <CardTitle className="text-2xl flex items-center justify-center gap-2">
                <MapPin className="w-6 h-6" />
                Where would you like to go?
              </CardTitle>
            </CardHeader>
            <CardContent className="p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <div className="mx-auto w-fit">
                    <label className="text-sm font-medium text-gray-600 flex items-center gap-2">
                      <Heart className="w-4 h-4 text-red-500" />
                      Describe your dream trip
                    </label>
                  </div>
                  <Textarea
                    value={request}
                    onChange={(e) => setRequest(e.target.value)}
                    placeholder="e.g., I want a 5-day trip to Rome with history and food, or a relaxing week in Bali with beaches and spa..."
                    className="min-h-[120px] resize-none border-2 border-teal-400 focus:border-amber-500 transition-colors"
                    disabled={loading}
                  />
                </div>

                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    type="submit"
                    disabled={loading || !request.trim()}
                    className="w-full bg-gradient-to-r from-teal-400 to-amber-400 hover:from-amber-400 hover:to-teal-400 text-white font-semibold py-4 text-lg shadow-lg"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                        Planning your adventure...
                      </>
                    ) : (
                      <>
                        <Search className="w-5 h-5 mr-2" />
                        Plan My Trip
                      </>
                    )}
                  </Button>
                </motion.div>
              </form>
            </CardContent>
          </Card>
        </motion.div>

        {/* Error Message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-4xl mx-auto mt-6"
            >
              <Card className="border-red-200 bg-red-50">
                <CardContent className="p-4">
                  <p className="text-red-600 text-center">{error}</p>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {response && (
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.8 }}
              className="max-w-6xl mx-auto mt-8 space-y-8"
            >
              {/* Trip Overview */}
              {response.destination_info && (
                <motion.div
                  initial={{ x: -100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <Card className="bg-gradient-to-r from-teal-500 to-teal-500 text-white shadow-2xl">
                    <CardContent className="p-8">
                      <div className="grid md:grid-cols-3 gap-6">
                        <div className="flex items-center gap-3">
                          <MapPin className="w-8 h-8" />
                          <div>
                            <p className="text-sm opacity-90">Destination</p>
                            <p className="text-xl font-bold">{response.destination_info.destination}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <Calendar className="w-8 h-8" />
                          <div>
                            <p className="text-sm opacity-90">Duration</p>
                            <p className="text-xl font-bold">{response.destination_info.duration} days</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <Users className="w-8 h-8" />
                          <div>
                            <p className="text-sm opacity-90">Style</p>
                            <p className="text-xl font-bold capitalize">{response.destination_info.travel_style}</p>
                          </div>
                        </div>
                      </div>

                      {response.destination_info.interests && (
                        <div className="mt-6">
                          <p className="text-sm opacity-90 mb-3">Your Interests</p>
                          <div className="flex flex-wrap gap-2">
                            {response.destination_info.interests.map((interest, index) => {
                              const IconComponent = interestIcons[interest as keyof typeof interestIcons] || Camera
                              return (
                                <motion.div
                                  key={interest}
                                  initial={{ scale: 0 }}
                                  animate={{ scale: 1 }}
                                  transition={{ delay: 0.1 * index }}
                                >
                                  <Badge className="bg-white/20 text-white border-white/30 px-3 py-1 flex items-center gap-1">
                                    <IconComponent className="w-4 h-4" />
                                    {interest}
                                  </Badge>
                                </motion.div>
                              )
                            })}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              )}

              <div className="grid lg:grid-cols-3 gap-8">
                {/* Itinerary */}
                <motion.div
                  initial={{ x: -100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                  className="lg:col-span-2"
                >
                  <Card className="bg-white/95 backdrop-blur-sm shadow-xl">
                    <CardHeader className="bg-gradient-to-r from-teal-400 to-amber-400 text-white">
                      <CardTitle className="flex items-center gap-2">
                        <Calendar className="w-6 h-6" />
                        Your Itinerary
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-8">
                      <div className="prose prose-lg max-w-none">{formatItinerary(response.itinerary)}</div>
                    </CardContent>
                  </Card>
                </motion.div>

                {/* Places */}
                <motion.div initial={{ x: 100, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.6 }}>
                  <Card className="bg-white/95 backdrop-blur-sm shadow-xl">
                    <CardHeader className="bg-gradient-to-r from-amber-400 to-teal-400 text-white">
                      <CardTitle className="flex items-center gap-2">
                        <MapPin className="w-6 h-6" />
                        Recommended Places
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        {response.places.map((place, index) => (
                          <motion.div
                            key={index}
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ delay: 0.1 * index }}
                            className="p-4 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100 hover:from-blue-50 hover:to-purple-50 transition-all duration-300 border border-gray-200 hover:border-blue-300"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <h3 className="font-semibold text-gray-800 mb-1">{place.name}</h3>
                                {place.rating && (
                                  <div className="flex items-center gap-1 mb-2">
                                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                                    <span className="text-sm font-medium text-gray-600">{place.rating}/5</span>
                                  </div>
                                )}
                                {place.description && <p className="text-sm text-gray-600 mb-2">{place.description}</p>}
                                <Badge variant="secondary" className="text-xs">
                                  {place.type.replace("_", " ")}
                                </Badge>
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="bg-white/80 backdrop-blur-md border-t border-white/20 mt-16"
      >
        <div className="container mx-auto px-4 py-8 text-center">
          <p className="text-gray-600">Made with ❤️ using AI • Plan your next adventure today!</p>
        </div>
      </motion.footer>
    </div>
  )
}
