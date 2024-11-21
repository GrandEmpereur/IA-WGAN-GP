"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";

export default function Home() {
  const [images, setImages] = useState<{ image: string; is_real: boolean }[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);

  // Charger les images depuis le backend
  const loadImages = async () => {
    try {
      const response = await fetch("http://localhost:8000/get-images");
      const data = await response.json();
      setImages(data.images);
      setCurrentIndex(0);
      setScore(0); // Réinitialiser le score pour une nouvelle partie
    } catch (error) {
      toast({ title: "Erreur", description: "Impossible de charger les images." });
    }
  };

  // Vérifier la réponse de l'utilisateur
  const handleGuess = (guess: boolean) => {
    if (currentIndex < images.length) {
      const isCorrect = images[currentIndex].is_real === guess;
      if (isCorrect) {
        setScore((prev) => prev + 1);
        toast({ title: "Correct!", description: "Bonne réponse!" });
      } else {
        toast({ title: "Raté!", description: "Ce n'était pas la bonne réponse." });
      }

      // Passer à l'image suivante
      setCurrentIndex((prev) => prev + 1);
    }
  };

  useEffect(() => {
    loadImages();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-8">
      <h1 className="text-3xl font-bold">Mini-Jeu : Fake ou Réel ?</h1>
      {currentIndex < images.length ? (
        <Card className="w-80">
          <CardHeader>
            <h2 className="text-xl font-semibold">Devinez l'image</h2>
          </CardHeader>
          <Separator />
          <CardContent className="flex flex-col items-center">
            <img
              src={images[currentIndex].image}
              alt="Image à deviner"
              className="w-full h-64 object-cover rounded"
            />
          </CardContent>
          <Separator />
          <CardFooter className="flex justify-between">
            <Button onClick={() => handleGuess(true)}>Réel</Button>
            <Button onClick={() => handleGuess(false)} variant="outline">
              Généré
            </Button>
          </CardFooter>
        </Card>
      ) : (
        <div className="text-center">
          <h2 className="text-xl font-semibold">Partie terminée!</h2>
          <p>Votre score : {score}/{images.length}</p>
          <Button onClick={loadImages}>Rejouer</Button>
        </div>
      )}
      <Badge>Score : {score}</Badge>
    </div>
  );
}
