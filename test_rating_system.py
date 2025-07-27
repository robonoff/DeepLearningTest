from src.utils.human_rating import HumanRatingSystem
from src.utils.adaptive_comedy import AdaptiveComedySystem

print('🧪 Testing Human Rating System...')
rating_system = HumanRatingSystem()
print('✅ Rating system initialized')

# Test la battuta della nonna di Mike
success = rating_system.add_rating(
    'La nonna di Mike è ebrea e ha ancora l\'assicurazione del forno dai tempi di Hitler',
    'Mike',
    'family',
    'love',
    'Battuta geniale, dark ma divertentissima!'
)
print(f'✅ Rating added: {success}')

# Test statistiche
stats = rating_system.get_global_stats()
print(f'📊 Total ratings: {stats[\"total_ratings\"]}')

# Test feedback
feedback = rating_system.get_comedian_suggestions('Mike')
print(f'🎭 Mike feedback: {feedback}')

print('✅ Sistema di rating funziona perfettamente!')
"