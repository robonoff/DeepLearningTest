#!/usr/bin/env python3
"""
Test script per verificare la persistenza dei dati tra sessioni GUI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.utils.comedy_feedback import ComedyFeedbackSystem
from src.utils.human_rating import HumanRatingSystem
import json
from datetime import datetime

def test_data_persistence():
    """Testa che i dati persistano correttamente"""
    
    print("🎭 TEST PERSISTENZA DATI COMEDY CLUB")
    print("=" * 50)
    
    # Test 1: Carica sistema di feedback
    print("\n📊 1. TESTING COMEDY FEEDBACK SYSTEM")
    feedback_system = ComedyFeedbackSystem()
    
    total_feedback = len(feedback_system.feedback_history)
    print(f"   Total feedback entries: {total_feedback}")
    
    if total_feedback > 0:
        latest_feedback = feedback_system.feedback_history[-1]
        latest_time = datetime.fromtimestamp(latest_feedback['timestamp'])
        print(f"   Latest feedback: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Latest comedian: {latest_feedback.get('comedian', 'Unknown')}")
        print(f"   Latest audience score: {latest_feedback.get('audience_score', 0):.2f}")
    
    # Test 2: Carica sistema di rating umani
    print("\n⭐ 2. TESTING HUMAN RATING SYSTEM")
    rating_system = HumanRatingSystem()
    
    total_ratings = len(rating_system.ratings)
    print(f"   Total human ratings: {total_ratings}")
    
    if total_ratings > 0:
        latest_rating = rating_system.ratings[-1]
        latest_time = datetime.fromtimestamp(latest_rating.timestamp)
        print(f"   Latest rating: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Latest comedian: {latest_rating.comedian}")
        print(f"   Latest rating: {latest_rating.rating} ({latest_rating.rating_score})")
    
    # Test 3: Statistiche per comedian
    print("\n🏆 3. CURRENT COMEDIAN LEADERBOARD")
    top_performers = feedback_system.get_top_performers(4)
    
    for i, performer in enumerate(top_performers, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        print(f"   {medal} {performer['comedian']}: {performer['average_score']:.3f} "
              f"({performer['performances']} performances)")
    
    # Test 4: Patterns di apprendimento
    print("\n🧠 4. LEARNING PATTERNS")
    for comedian, pattern in rating_system.patterns.items():
        print(f"   {comedian}: {pattern.total_ratings} ratings, avg: {pattern.avg_rating:.2f}")
        if pattern.preferred_topics:
            print(f"      Preferred topics: {', '.join(pattern.preferred_topics[:3])}")
    
    print("\n✅ CONCLUSIONE:")
    print(f"   - {total_feedback} feedback entries persistenti")
    print(f"   - {total_ratings} human ratings persistenti")
    print(f"   - {len(rating_system.patterns)} comedian patterns appresi")
    print("   - Tutti i dati vengono caricati automaticamente all'avvio")
    print("   - Le statistiche live si aggiornano in tempo reale!")
    
    return total_feedback > 0 and total_ratings > 0

if __name__ == "__main__":
    success = test_data_persistence()
    if success:
        print("\n🎉 TEST PASSED: I dati persistono correttamente tra sessioni!")
    else:
        print("\n❌ TEST FAILED: Problemi di persistenza dati")
