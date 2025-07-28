#!/usr/bin/env python3
"""
Test script per il sistema RAG del Comedy Club
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_rag_system():
    """Test the enhanced RAG system"""
    print("🧪 Testing Enhanced RAG System...")
    
    try:
        from src.utils.enhanced_joke_rag import EnhancedJokeRAG
        
        rag = EnhancedJokeRAG()
        
        if not rag.is_available():
            print("❌ RAG system not available. Run: python scripts/generate_embeddings.py")
            return False
        
        # Test senza web search
        print("\n🔍 Test ricerca locale...")
        result = rag.retrieve_jokes_with_context("observational humor", "smartphones", use_web_search=False)
        print(f"✅ RAG locale funziona: {len(result['jokes'])} jokes trovati")
        
        if result['jokes']:
            print("   Sample joke:", result['jokes'][0][:100] + "...")
        
        # Test con web search
        print("\n🌐 Test ricerca con web search...")
        result = rag.retrieve_jokes_with_context("observational humor", "smartphones", use_web_search=True)
        print(f"✅ RAG con web search funziona: {len(result['jokes'])} jokes")
        print(f"   Contesto web: {len(result['web_context'])} caratteri")
        
        if result['web_context']:
            print("   Sample context:", result['web_context'][:100] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test RAG fallito: {e}")
        return False

def test_comedy_club_integration():
    """Test integrazione completa con ComedyClub"""
    print("\n🎭 Test integrazione Comedy Club...")
    
    try:
        from src.core.comedy_club_clean import ComedyClub
        
        # Test con web search
        club = ComedyClub(use_web_search=True)
        print("✅ ComedyClub inizializzato con web search")
        
        # Test senza web search
        club_offline = ComedyClub(use_web_search=False)
        print("✅ ComedyClub inizializzato in modalità offline")
        
        # Test generazione joke
        joke = club.get_joke(topic="technology")
        print("✅ Generazione joke con RAG funziona")
        print(f"   Joke: {joke[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test integrazione fallito: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test Sistema RAG per Comedy Club")
    print("=" * 50)
    
    success1 = test_rag_system()
    success2 = test_comedy_club_integration()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ Tutti i test passati!")
        print("💡 Il sistema RAG è pronto all'uso")
    else:
        print("❌ Alcuni test falliti")
        print("💡 Esegui: python scripts/generate_embeddings.py")
        print("💡 Installa: pip install sentence-transformers scikit-learn duckduckgo-search")
    
    sys.exit(0 if (success1 and success2) else 1)
