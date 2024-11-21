"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";

export default function Home() {
  const [image, setImage] = useState<string | null>(null);
  const [isReal, setIsReal] = useState<boolean | null>(null); // null = pas encore deviné
  const [score, setScore] = useState(0);

  // Charger une image générée depuis l'API Flask
  const loadImage = async () => {
    try {
      const response = await fetch("http://localhost:8000/generate", { method: "POST" });
      const data = await response.json();
      setImage(data.image);
    } catch (error) {
      toast({ title: "Erreur", description: "Impossible de charger l'image." });
    }
  };

  // Vérifier la réponse de l'utilisateur
  const handleGuess = (guess: boolean) => {
    if (isReal === guess) {
      setScore((prev) => prev + 1);
      toast({ title: "Bravo!", description: "Vous avez deviné correctement." });
    } else {
      toast({ title: "Raté!", description: "Ce n'était pas la bonne réponse." });
    }
    loadImage(); // Charger une nouvelle image
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-8">
      <h1 className="text-3xl font-bold">Mini-Jeu : Fake ou Réel ?</h1>
      <Card className="w-80">
        <CardHeader>
          <h2 className="text-xl font-semibold">Devinez l'image</h2>
        </CardHeader>
        <Separator />
        <CardContent className="flex flex-col items-center">
          {image ? (
    <img
        src={image} // Utilisation directe de la chaîne retournée
        alt="Image générée"
        className="w-full h-64 object-cover rounded"
    />
) : (
    <p className="text-muted">Cliquez sur "Commencer" pour charger une image.</p>
)}

        </CardContent>
        <Separator />
        <CardFooter className="flex justify-between">
          <Button onClick={() => handleGuess(true)}>Réel</Button>
          <Button onClick={() => handleGuess(false)} variant="outline">
            Généré
          </Button>
        </CardFooter>
      </Card>
      <Badge>Score : {score}</Badge>
      <Button onClick={loadImage}>Commencer</Button>
    </div>
  );
}
