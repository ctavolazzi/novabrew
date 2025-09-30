#!/bin/bash

# ============================================
# 🚀 ULTIMATE MODEL TESTING SUITE 🚀
# Tests both models under extreme conditions
# ============================================
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
TEST_DIR="src/tests/results/${TIMESTAMP}"
mkdir -p "$TEST_DIR"

# Function to run test and save result
run_test() {
    local test_name=$1
    local model=$2
    local prompt=$3
    local test_number=$4
    local temperature=${5:-0.7}

    echo "🧪 Running Test $test_number: $test_name on $model..."

    # Pre-test metrics
    local start_time=$(date +%s%N)
    local start_mem=$(vm_stat | grep "Pages free:" | awk '{print $3}')

    # Run test with timeout protection
    response=$(timeout 30s curl -s http://localhost:11434/api/generate -d "{
      \"model\": \"$model\",
      \"prompt\": $prompt,
      \"stream\": false,
      \"options\": {
        \"temperature\": $temperature,
        \"top_p\": 0.9,
        \"num_predict\": 500
      }
    }")

    # Check if test timed out
    if [ $? -eq 124 ]; then
        echo "⚠️ Test timed out after 30 seconds!"
        response="{\"error\": \"timeout\"}"
    fi

    # Post-test metrics
    local end_time=$(date +%s%N)
    local duration=$(( ($end_time - $start_time) / 1000000 ))

    # Save result with timestamp
    echo "{
      \"test_number\": $test_number,
      \"test_name\": \"$test_name\",
      \"model\": \"$model\",
      \"timestamp\": \"$(date +"%Y-%m-%d %H:%M:%S")\",
      \"duration_ms\": $duration,
      \"response\": $response
    }" > "$TEST_DIR/test_${test_number}_${model}.json"

    echo "✅ Test $test_number completed in ${duration}ms"
}

# ============================================
# 🧪 HARDCORE TEST SUITE
# ============================================
echo "🚀 Starting Ultimate Model Tests..."

# Test 1: Basic Sanity Check
echo "📝 Test 1: Basic JSON (Sanity Check)"
run_test "Basic JSON" "nemotron-mini" '"Return this exact JSON: {\"test\": \"hello\"}"' 1 0.1
run_test "Basic JSON" "llama3.2" '"Return this exact JSON: {\"test\": \"hello\"}"' 1 0.1

# Test 2: Complex Game Scene
echo "🎮 Test 2: Complex Game Scene"
run_test "Game Scene" "nemotron-mini" '"Generate a complex game scene with 3 choices. Must be valid JSON with this structure: {\"scene\": {\"title\": \"Scene Title\", \"description\": \"Scene description\"}, \"choices\": [{\"text\": \"Choice description\", \"healthEffect\": number between -20 and 20, \"manaEffect\": number between -20 and 20}]}"' 2 0.7

# Test 3: Story Continuation
echo "📚 Test 3: Story Continuation"
run_test "Story" "nemotron-mini" '"Previous scene: \"A dark forest path lies ahead.\" Player chose: \"Walk carefully forward.\" Return valid JSON with new scene and 3 choices."' 3 0.7

# Test 4: Error Recovery
echo "🐛 Test 4: Error Recovery"
run_test "Error" "nemotron-mini" '"Complete this JSON: {\"scene\": {\"title\": \"Test"' 4 0.1

# Test 5: Long Response
echo "📜 Test 5: Long Response"
run_test "Long" "nemotron-mini" '"Generate an epic fantasy scene with detailed description and 5 complex choices. Must be valid JSON."' 5 0.9

# Test 6: Speed Test
echo "⚡ Test 6: Speed Test"
run_test "Speed" "nemotron-mini" '"Quick response needed! Return: {\"test\": \"speed\"}"' 6 0.1

# Test 7: Memory Test
echo "💾 Test 7: Memory Test"
run_test "Memory" "nemotron-mini" '"Generate a massive game world with 10 interconnected scenes. Must be valid JSON."' 7 0.7

# Test 8: Edge Case
echo "🔥 Test 8: Edge Case"
run_test "Edge" "nemotron-mini" '"Generate the longest possible valid JSON response you can with multiple nested objects and arrays."' 8 1.0

# Generate summary report
echo "📊 Generating test summary..."
echo "# 🚀 Model Test Results - $(date)
## Overview
- Total Tests: 8
- Models: nemotron-mini, llama3.2
- Test Directory: $TEST_DIR

## Results
$(for f in "$TEST_DIR"/test_*.json; do
    echo "### $(basename "$f")"
    cat "$f" | jq '.'
    echo
done)" > "$TEST_DIR/summary.md"

echo "
🏁 Testing Complete!
📂 Results saved to: $TEST_DIR
📊 View summary at: $TEST_DIR/summary.md
"

# Quick stats
echo "📈 Quick Stats:"
echo "Fastest response: $(find "$TEST_DIR" -name "test_*.json" -exec jq '.duration_ms' {} \; | sort -n | head -n1)ms"
echo "Slowest response: $(find "$TEST_DIR" -name "test_*.json" -exec jq '.duration_ms' {} \; | sort -n | tail -n1)ms"
echo "Average response: $(find "$TEST_DIR" -name "test_*.json" -exec jq '.duration_ms' {} \; | awk '{ sum += $1 } END { print sum/NR }')ms"
