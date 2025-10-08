#!/bin/bash

# List of supported Java versions
SUPPORTED_VERSIONS="8 11 17 21"
# Default priority order
DEFAULT_PRIORITY="8 11 17 21"

# Define candidates for each version as multi-line variables
JAVA8_CANDIDATES="/usr/java/jdk8u432-b06
/usr/lib/jvm/java-8-openjdk
/usr/lib/jvm/java-1.8.0-openjdk
/usr/lib/jvm/jdk1.8
/usr/lib/jvm/jre1.8
/usr/java/jdk1.8
/usr/java/jre1.8
/usr/lib/jvm/jre-1.8.0
/usr/lib/jvm/jre-1.8.0-openjdk
/Library/Java/JavaVirtualMachines/jdk1.8.*.jdk/Contents/Home
$HOME/java/jdk1.8"

JAVA11_CANDIDATES="/usr/lib/jvm/java-11-openjdk
/usr/lib/jvm/jdk-11
/usr/java/jdk-11
/usr/lib/jvm/temurin-11-jdk
/Library/Java/JavaVirtualMachines/jdk-11.*.jdk/Contents/Home
$HOME/java/jdk-11"

JAVA17_CANDIDATES="/usr/lib/jvm/java-17-openjdk
/usr/lib/jvm/jdk-17
/usr/java/jdk-17
/usr/lib/jvm/temurin-17-jdk
/home/jdk-17.0.15/
/Library/Java/JavaVirtualMachines/jdk-17.*.jdk/Contents/Home
$HOME/java/jdk-17"

JAVA21_CANDIDATES="/usr/lib/jvm/java-21-openjdk
/usr/lib/jvm/jdk-21
/usr/java/jdk-21
/usr/lib/jvm/temurin-21-jdk
/usr/lib/jvm/jdk-21.0.8-oracle-aarch64
/Library/Java/JavaVirtualMachines/jdk-21.*.jdk/Contents/Home
$HOME/java/jdk-21"

# Initialize variables to store found paths
JAVA8_HOME=""
JAVA11_HOME=""
JAVA17_HOME=""
JAVA21_HOME=""

# Check command line argument for requested version
requested_version=""
if [ $# -gt 0 ]; then
    if echo " $SUPPORTED_VERSIONS " | grep -q " $1 "; then
        requested_version=$1
        echo "Prioritizing Java version $requested_version..."
    else
        echo "Warning: Version $1 is not supported. Using default priority."
        echo "Supported versions: $SUPPORTED_VERSIONS"
    fi
fi

# Function to detect Java version
detect_java() {
    local version=$1
    shift
    local candidates="$@"

    # Iterate through candidate paths
    while IFS= read -r candidate; do
        [ -z "$candidate" ] && continue

        # Handle wildcard paths
        for path in $(ls -d "$candidate" 2>/dev/null); do
            if [ -x "$path/bin/java" ]; then
                # Get version information
                java_version=$("$path/bin/java" -version 2>&1 | awk -F '"' '/version/ {print $2}')
                major_version=$(echo "$java_version" | cut -d '.' -f 1)

                # Special handling for Java 8 (1.8.x format)
                if [ "$major_version" = "1" ]; then
                    major_version=$(echo "$java_version" | cut -d '.' -f 2)
                fi

                # Verify version matches
                if [ "$major_version" -eq "$version" ]; then
                    echo "$path"
                    return 0
                fi
            fi
        done
    done <<< "$candidates"

    return 1
}

# Detect each Java version
echo "Searching for Java installations..."
JAVA8_HOME=$(detect_java 8 "$JAVA8_CANDIDATES")
JAVA11_HOME=$(detect_java 11 "$JAVA11_CANDIDATES")
JAVA17_HOME=$(detect_java 17 "$JAVA17_CANDIDATES")
JAVA21_HOME=$(detect_java 21 "$JAVA21_CANDIDATES")

# Display found versions
echo -e "\nDiscovered Java versions:"
[ -n "$JAVA8_HOME" ] && echo "  Java 8: $JAVA8_HOME"
[ -n "$JAVA11_HOME" ] && echo "  Java 11: $JAVA11_HOME"
[ -n "$JAVA17_HOME" ] && echo "  Java 17: $JAVA17_HOME"
[ -n "$JAVA21_HOME" ] && echo "  Java 21: $JAVA21_HOME"

# Determine which version to use
selected_home=""
if [ -n "$requested_version" ]; then
    case $requested_version in
        8) [ -n "$JAVA8_HOME" ] && selected_home="$JAVA8_HOME" ;;
        11) [ -n "$JAVA11_HOME" ] && selected_home="$JAVA11_HOME" ;;
        17) [ -n "$JAVA17_HOME" ] && selected_home="$JAVA17_HOME" ;;
        21) [ -n "$JAVA21_HOME" ] && selected_home="$JAVA21_HOME" ;;
    esac

    if [ -z "$selected_home" ]; then
        echo -e "\nRequested version $requested_version not found. Using default priority."
    fi
fi

# If no requested version or not found, use default priority
if [ -z "$selected_home" ]; then
    for version in $DEFAULT_PRIORITY; do
        case $version in
            8) [ -n "$JAVA8_HOME" ] && selected_home="$JAVA8_HOME" && break ;;
            11) [ -n "$JAVA11_HOME" ] && selected_home="$JAVA11_HOME" && break ;;
            17) [ -n "$JAVA17_HOME" ] && selected_home="$JAVA17_HOME" && break ;;
            21) [ -n "$JAVA21_HOME" ] && selected_home="$JAVA21_HOME" && break ;;
        esac
    done
fi

# Set JAVA_HOME if found
if [ -n "$selected_home" ]; then
    export JAVA_HOME="$selected_home"
    echo -e "\nJAVA_HOME set to: $JAVA_HOME"
    exit 0
else
    echo -e "\nError: No supported Java versions found." >&2
    exit 1
fi
