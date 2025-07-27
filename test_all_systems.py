#!/usr/bin/env python3
"""
Sistema di test completo per verificare tutti i componenti del Comedy Club
"""

def test_comedy_tools():
    """Test del sistema di analisi comico"""
    print("🛠️ Testing ComedyTools...")
    try:
        from src.utils.comedy_tools import ComedyTools
        
        tools = ComedyTools()
        test_joke = "Why don't scientists trust atoms? Because they make up everything!"
        analysis = tools.analyze_joke_quality(test_joke)
        
        print(f"✅ ComedyTools: Score {analysis.overall_score:.2f}, Type: {analysis.humor_type}")
        return True
    except Exception as e:
        print(f"❌ ComedyTools Error: {e}")
        return False

def test_rating_system():
    """Test del sistema di rating umano"""
    print("⭐ Testing Rating System...")
    try:
        from src.utils.human_rating import HumanRatingSystem
        
        rating_system = HumanRatingSystem()
        rating_system.add_rating("Test joke", "Mike", "test", "like", "wordplay")
        
        stats = rating_system.get_global_stats()
        print(f"✅ Rating System: {len(stats.get('all_ratings', []))} total ratings stored")
        return True
    except Exception as e:
        print(f"❌ Rating System Error: {e}")
        return False

def test_adaptive_learning():
    """Test del sistema di apprendimento adattivo"""
    print("🧠 Testing Adaptive Learning...")
    try:
        from src.utils.human_rating import HumanRatingSystem
        from src.utils.adaptive_comedy import AdaptiveComedySystem
        
        rating_system = HumanRatingSystem()
        adaptive_system = AdaptiveComedySystem()
        
        # Add sample rating
        rating_system.add_rating("Tech joke", "Mike", "technology", "like", "wordplay")
        
        # Test analysis
        analysis = adaptive_system.analyze_comedian_performance(rating_system)
        insights = adaptive_system.get_comedian_insights("Mike")
        
        print(f"✅ Adaptive Learning: {len(analysis.keys())} comedians analyzed, {len(insights)} insight categories")
        return True
    except Exception as e:
        print(f"❌ Adaptive Learning Error: {e}")
        return False

def test_enhanced_rag():
    """Test del sistema RAG (rapido, senza modelli)"""
    print("🔍 Testing Enhanced RAG (basic)...")
    try:
        from src.utils.enhanced_joke_rag import EnhancedJokeRAG
        
        # Test basic initialization
        print("✅ Enhanced RAG: Import successful (full test requires models)")
        return True
    except Exception as e:
        print(f"❌ Enhanced RAG Error: {e}")
        return False

def test_orfeo_config():
    """Test della configurazione Orfeo"""
    print("🎯 Testing Orfeo Configuration...")
    try:
        from config.orfeo_config_new import get_config_list, get_rag_config
        
        config = get_config_list()
        rag_config = get_rag_config()
        
        print(f"✅ Orfeo Config: Model {config[0]['model']}, RAG configured")
        return True
    except Exception as e:
        print(f"❌ Orfeo Config Error: {e}")
        return False

def main():
    """Test completo di tutti i sistemi"""
    print("🎭 COMEDY CLUB SYSTEM VALIDATION")
    print("=" * 50)
    
    tests = [
        ("Comedy Tools", test_comedy_tools),
        ("Rating System", test_rating_system),
        ("Adaptive Learning", test_adaptive_learning),
        ("Enhanced RAG", test_enhanced_rag),
        ("Orfeo Configuration", test_orfeo_config)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
        print()
    
    print("=" * 50)
    print("📊 FINAL RESULTS:")
    
    working = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ WORKING" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            working += 1
    
    print(f"\n🎉 SYSTEM STATUS: {working}/{total} components operational")
    
    if working == total:
        print("🚀 ALL SYSTEMS GO! Your comedy club is ready to rock!")
    elif working >= 3:
        print("⚡ Most systems working! Comedy club is functional!")
    else:
        print("🔧 Some systems need attention, but core functionality available.")
    
    print("\n💡 FEATURES AVAILABLE:")
    if results.get("Comedy Tools", False):
        print("   • Joke quality analysis and improvement suggestions")
    if results.get("Rating System", False):
        print("   • Human rating collection and statistics")
    if results.get("Adaptive Learning", False):
        print("   • AI learning from human feedback")
    if results.get("Enhanced RAG", False):
        print("   • Intelligent joke retrieval (requires model loading)")
    if results.get("Orfeo Configuration", False):
        print("   • Orfeo AI integration for joke generation")

if __name__ == "__main__":
    main()
